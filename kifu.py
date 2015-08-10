#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
from optparse import OptionParser
import yaml
import logging
from sys import platform as _platform

k_appname = 'kifu'

logger = logging.getLogger(k_appname)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

options = {}
unix_app_socket = "app.sock"
project_name_placeholder = "~~~PROJNAME~~~"
base_dir = None
abs_env_dir = None
abs_root_dir = None
settings = None

def main():
    global base_dir
    global abs_env_dir
    global options
    global settings

    parser = OptionParser()
    parser.add_option("-n", "--name", dest="project_name", type="string", help="Name of the new pyramid project.")
    parser.add_option("-d", "--deploy", dest="deploy_dir", type="string", help="Deploy base directory of webapp.")
    parser.add_option("-s", "--supervisor-enabled", action="store_true", dest="supervisor_enabled", help="Run gunicorn with supervisor.")
    parser.add_option("-b", "--database", dest="database_type", type="string", help="Database type. sqlite or postgresql")
    parser.add_option("-p", "--python", dest="python_path", type="string", help="Path to python to use for virtualenv")

    (options, args) = parser.parse_args()

    argc = len(sys.argv[1:])

    base_dir = os.getcwd();
    
    if options.project_name is None:
        options.project_name = "default"

    if options.deploy_dir is None:
        options.deploy_dir = base_dir

    if options.supervisor_enabled is None:
        options.supervisor_enabled = False

    if options.database_type is None:
        options.database_type = "sqlite"

    print("options.database_type: " + options.database_type)
    with open(k_appname + '.yaml') as f:
        settings = yaml.load(f)

    absolute_deploydir = os.path.abspath(options.deploy_dir)
    os.chdir(absolute_deploydir)

    virtualenv_cmd = None
    if options.python_path is None:
        virtualenv_cmd = ["virtualenv", options.project_name + "_env"]
    else:
        virtualenv_cmd = ["virtualenv", "--python=" + options.python_path, options.project_name + "_env"]

    subprocess.call(virtualenv_cmd)

    abs_env_dir = os.path.abspath(os.path.join(absolute_deploydir, options.project_name + "_env"))
    os.chdir(abs_env_dir)

    setup_rabbitmq()
    perform_installs()

    abs_root_dir = os.path.join(abs_env_dir, options.project_name)
    os.chdir(abs_root_dir)

    print("abs_env_dir: " + abs_env_dir)
    print("getcwd: " + os.getcwd())
    print("base_dir: " + base_dir)

    setup_maininitpy()
    setup_dotini()
    setup_packages()
    setup_tests()

    subprocess.call(["../bin/python", "setup.py", "develop"])


    # change all ~~~PROJNAME~~~ to actual name
    full_file_paths = _get_filepaths(abs_root_dir)

    for f in full_file_paths:
        if f.endswith(".py") or f.endswith("mako" or f.endswith("conf")):
            substitute_in_file(f, "~~~PROJNAME~~~", options.project_name)


    substitute_in_file(os.path.join(abs_root_dir, "development.ini"), "    pyramid_debugtoolbar", "#   pyramid_debugtoolbar")
    setup_alembic()

    if options.supervisor_enabled:

        output_nginx_help()
        # Install supervisord and run
        os.system("../bin/pip install supervisor")

        # Copy supervisord.conf file to new environment
        shutil.copy(base_dir + "/supervisord.conf", abs_root_dir)
        substitute_in_file(os.path.join(abs_root_dir, "supervisord.conf"), "~~~PROJNAME~~~", options.project_name)

        os.system("../bin/supervisord -n -c supervisord.conf")
    else:
        os.system("../bin/gunicorn --paster production.ini --bind unix:app.sock --workers 4")

def prepend_in_file(filepath, string):
    with open(filepath, 'r') as original: data = original.read()
    with open(filepath, 'w') as modified: modified.write(string + data)

def substitute_in_file(filename, old_string, new_string):
    s=open(filename).read()
    if old_string in s:
            logger.info('Changing "{old_string}" to "{new_string}" in "{filename}"'.format(**locals()))
            s=s.replace(old_string, new_string)
            f=open(filename, 'w')
            f.write(s)
            f.flush()
            f.close()
    else:
            logger.info('No occurences of "{old_string}" found in "{filename}" '.format(**locals()))

def setup_rabbitmq():
    global options
    
    rabbitmq_user = options.project_name + '_user'
    
    subprocess.call(['rabbitmqctl', 'add_user', rabbitmq_user, options.project_name]) #project name is the password
    subprocess.call(['rabbitmqctl', 'add_vhost', options.project_name])
    subprocess.call(['rabbitmqctl', 'set_permissions', '-p', options.project_name, rabbitmq_user, '.*', '.*', '.*'])    
    
def perform_installs():
    global abs_env_dir
    global options

    # Install pyramid_alembic_mako
    # subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(['bin/pip', 'install','pyramid'])
    subprocess.call(['bin/pip', 'install','setuptools_git'])
    # subprocess.call(["bin/easy_install", "setuptools_git"])
    subprocess.call(["git", "clone", "https://github.com/inklesspen/pyramid_alembic_mako.git"])
    os.chdir(os.path.abspath(os.path.join(abs_env_dir, "pyramid_alembic_mako")))
    os.system("../bin/pip install .")

    os.chdir(abs_env_dir)
    subprocess.call(["bin/pcreate", "-s", "alembic_mako", options.project_name])

    # treat bcrypt special when on mac os x from an issue introduced in Xcode 5.1: http://stackoverflow.com/a/22322645/841065
    if _platform == "darwin":
        logger.info("darwin")
        os.environ["CPPFLAGS"] = "-Qunused-arguments"
        os.environ["CFLAGS"] = "-Qunused-arguments"

    subprocess.call(["bin/pip", "install", "bcrypt"])

    # subprocess.call(["bin/easy_install", "celery"])
    subprocess.call(['bin/pip', 'install','celery'])
    # subprocess.call(["bin/easy_install", "decorator"])
    subprocess.call(['bin/pip', 'install','decorator'])
    # subprocess.call(["bin/easy_install", "gunicorn"])
    subprocess.call(['bin/pip', 'install','gunicorn'])
    # subprocess.call(["bin/easy_install", "redis"])
    subprocess.call(['bin/pip', 'install','redis'])
    # subprocess.call(["bin/easy_install", "wtforms"])

    subprocess.call(["bin/pip", "install", "requests"])

    # subprocess.call(["bin/easy_install", "pyramid_mailer"])
    subprocess.call(['bin/pip', 'install','pyramid_mailer'])
    if options.database_type is "postgresql":
        # subprocess.call(["bin/easy_install", "psycopg2"])
        subprocess.call(['bin/pip', 'install','psycopg2'])

    # Install dependencies in requirements.txt
    #requirements = os.path.join(base_dir, "requirements.txt")
    #os.system("bin/pip install -r " + requirements)

def setup_maininitpy():
    global settings
    global abs_env_dir
    global abs_root_dir

    maininitpy_map = settings["maininitpy"]

    templateinclude = ("config.include(\"pyramid_mako\")")
    maininitpy = os.path.join(os.getcwd(), options.project_name + "/__init__.py")
    substitute_in_file(maininitpy, "config = Configurator(settings=settings)", templateinclude)
    # Tweak the main __init__.py to use the project name and correct models path
    substitute_in_file(maininitpy, "from .models import (", "from ~~~PROJNAME~~~.models import (")

    # Add os.path imports to __init__.py

    substitute_in_file(maininitpy, "def main(global_config, **settings):", maininitpy_map["userauth"])
    prepend_in_file(maininitpy, maininitpy_map["mainimports"])

    substitute_in_file(maininitpy, "    config.scan()", "    config.scan(\"~~~PROJNAME~~~.views\")")

    # We add routes via routes.py now, so remove this template code
    substitute_in_file(maininitpy, "    config.add_route(\'home\', \'/\')", "")

def setup_dotini():
    global abs_env_dir
    global abs_root_dir
    global options

    developmentini = os.path.abspath(os.path.join(os.getcwd(), "development.ini"))
    productionini = os.path.join(os.getcwd(), "production.ini")

    # Add template if it is in the yaml file
    #if settings["template"] != None:        
    
    substitute_in_file(developmentini, "pyramid.includes =", "pyramid.includes =\n    pyramid_mailer\n    pyramid_mako")
    substitute_in_file(productionini, "pyramid.includes =", "pyramid.includes =\n    pyramid_mailer\n    pyramid_mako")

    authsecret_orig = "sqlalchemy.url = sqlite:///%(here)s/" + options.project_name + ".sqlite"

    if options.database_type is "postgresql":
        authsecret_orig = "sqlalchemy.url = postgresql+psycopg2://PGUSERNAME:PGPASSWORD@localhost/" + options.project_name

    authsecret_subst = authsecret_orig + "\n\nauth.secret=PLEASECHANGEME\n\nsession.secret = PLEASECHANGEMETOO\n\nmail.host=smtp.mandrillapp.com\nmail.username=YOURMANDRILLAPPUSERNAME\nmail.password=YOURMANDRILLAPPPASSWORD\nmail.port=587\nmail.ssl=False\nmail.default_sender=donotreply@YOURDOMAIN"
    substitute_in_file(developmentini, authsecret_orig, authsecret_subst)
    substitute_in_file(productionini, authsecret_orig, authsecret_subst)
    substitute_in_file(productionini, "[server:main]", "[server:main]\nunix_socket = %(here)s/" + unix_app_socket + "\nhost = localhost\nport = 80\n")

def setup_packages():
    global options
    global base_dir
    global abs_env_dir
    global abs_root_dir


    print("abs_env_dir: " + abs_env_dir)
    print("getcwd: " + os.getcwd())
    print("base_dir: " + base_dir)

    # Copy Celery-related files to the app
    celery_dir = os.path.join(os.getcwd(), options.project_name + "/queue")
    shutil.copytree(base_dir + "/queue", celery_dir)

    # Copy models.py to the models package and rename it mymodel.py
    #shutil.copy(os.path.join(os.getcwd(), options.project_name + "/models.py"), base_dir + "/models/mymodel.py")

    # Copy models dir to the app
    models_dir = os.path.join(os.getcwd(), options.project_name + "/models")
    shutil.copytree(base_dir + "/models", models_dir)

    # Copy forms dir to the app
    # forms_dir = os.path.join(os.getcwd(), options.project_name + "/forms")
    # shutil.copytree(base_dir + "/forms", forms_dir)

    # Delete the unnecessary models.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/models.py"))

    ### lib ###

    # copy lib to project
    lib_dir = os.path.join(os.getcwd(), options.project_name + "/lib")
    shutil.copytree(base_dir + "/lib", lib_dir)

    ### celery ###

    # Tweak initialize db script to use replacement model hierarchy
    initializedbpy = os.path.join(os.getcwd(), options.project_name + "/scripts/initializedb.py")
    substitute_in_file(initializedbpy, "    MyModel,", "#    MyModel,")
    substitute_in_file(initializedbpy, "    with transaction.manager:", "#    with transaction.manager:")
    substitute_in_file(initializedbpy, "model = MyModel", "#model = MyModel")
    substitute_in_file(initializedbpy, "DBSession.add", "#DBSession.add")

    viewspy = os.path.join(os.getcwd(), options.project_name + "/views.py")

    # Delete views.py
    os.unlink(viewspy)
    #shutil.copy(os.path.join(os.getcwd(), options.project_name + "/views.py"), base_dir + "/views/home.py")

    # Copy views to the app
    views_dir = os.path.join(os.getcwd(), options.project_name + "/views")
    shutil.copytree(base_dir + "/views", views_dir)

    # Delete mymodel.py
    mymodelpy = os.path.join(os.getcwd(), options.project_name + "/models/mymodel.py")
    os.unlink(mymodelpy)

    # Copy over static css/js resources
    css_dir = os.path.join(os.getcwd(), options.project_name + "/static/css")
    shutil.copytree(base_dir + "/static/css", css_dir)
    img_dir = os.path.join(os.getcwd(), options.project_name + "/static/img")
    shutil.copytree(base_dir + "/static/img", img_dir)
    js_dir = os.path.join(os.getcwd(), options.project_name + "/static/js")
    shutil.copytree(base_dir + "/static/js", js_dir)
    fa_dir = os.path.join(os.getcwd(), options.project_name + "/static/font-awesome")
    shutil.copytree(base_dir + "/static/font-awesome", fa_dir)
    bootstrap_dir = os.path.join(os.getcwd(), options.project_name + "/static/bootstrap")
    shutil.copytree(base_dir + "/static/bootstrap", bootstrap_dir)
    jquery_dir = os.path.join(os.getcwd(), options.project_name + "/static/jquery")
    shutil.copytree(base_dir + "/static/jquery", jquery_dir)

    # Copy over templates
    accounts_dir = os.path.join(os.getcwd(), options.project_name + "/templates/accounts")
    shutil.copytree(base_dir + "/templates/accounts", accounts_dir)

    auth_dir = os.path.join(os.getcwd(), options.project_name + "/templates/auth")
    shutil.copytree(base_dir + "/templates/auth", auth_dir)

    layoutmako = base_dir + "/templates/layout.mako"
    list_usersmako = base_dir + "/templates/list_users.mako"

    # Copy over layout.mako
    shutil.copy(layoutmako, os.path.join(os.getcwd(), options.project_name + "/templates/layout.mako"))

    # Copy over routes.py
    routespy = base_dir + "/routes.py"
    shutil.copy(routespy, os.path.join(os.getcwd(), options.project_name + "/routes.py"))

    ### views ###

    viewsauthpy = base_dir + "/views/auth.py"
    # Copy over views auth.py
    shutil.copy(viewsauthpy, os.path.join(os.getcwd(), options.project_name + "/views/auth.py"))

    viewsaccountspy = base_dir + "/views/accounts.py"
    # Copy over views accounts.py
    shutil.copy(viewsaccountspy, os.path.join(os.getcwd(), options.project_name + "/views/accounts.py"))

    viewsapipy = base_dir + "/views/api.py"

    # Copy over views api.py
    shutil.copy(viewsapipy, os.path.join(os.getcwd(), options.project_name + "/views/api.py"))

    # Copy over a gitignore template
    gitignorefile = base_dir + "/gitignore"
    shutil.copy(gitignorefile, os.path.join(os.getcwd(), options.project_name + ".gitignore"))


def output_nginx_help():
    global options
    global unix_app_socket
    global abs_env_dir
    global abs_root_dir

    # Help text for configuring nginx
    print ("")
    print ("add to nginx http {} section:")
    print ("upstream "+ options.project_name + "-site {")
    print ("     server unix://" + os.path.abspath(unix_app_socket) + " fail_timeout=0;")
    print ("}")
    print ("")
    print ("add to nginx server {} section:")
    print ("server {")
    print ("")
    print ("    # optional ssl configuration")
    print ("")
    print ("    #listen 443 ssl;")
    print ("    #ssl_certificate /path/to/ssl/pem_file;")
    print ("    #ssl_certificate_key /path/to/ssl/certificate_key;")
    print ("")
    print ("    # end of optional ssl configuration")
    print ("    listen 80;")
    print ("    server_name _;")
    print ("")
    print ("    access_log  " + os.getcwd() + "/access.log;")
    print ("    error_log   " + os.getcwd() + "/error.log;")
    print ("")
    print ("    location /static/ {")
    print ("        root                    " + os.getcwd() + "/" + options.project_name + "/;")
    print ("        expires                 30d;")
    print ("        add_header              Cache-Control public;")
    print ("        access_log              off;")
    print ("    }")
    print ("")
    print ("")
    print ("    location / {")
    print ("        proxy_set_header        Host $http_host;")
    print ("        proxy_set_header        X-Real-IP $remote_addr;")
    print ("        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;")
    print ("        proxy_set_header        X-Forwarded-Proto $scheme;")
    print ("")
    print ("        client_max_body_size    10m;")
    print ("        client_body_buffer_size 128k;")
    print ("        proxy_connect_timeout   60s;")
    print ("        proxy_send_timeout      90s;")
    print ("        proxy_read_timeout      90s;")
    print ("        proxy_buffering         off;")
    print ("        proxy_temp_file_write_size 64k;")
    print ("        proxy_pass http://" + options.project_name + "-site;")
    print ("        proxy_redirect          off;")
    print ("    }")
    print ("}")

def setup_tests():
    global options
    global abs_env_dir
    global abs_root_dir

    # Tweak the tests.py to use the project name and correct models path
    testspy = os.path.join(os.getcwd(), options.project_name + "/tests.py")

    substitute_in_file(testspy, "from .models import DBSession", "from ~~~PROJNAME~~~.models.mymodel import DBSession")
    substitute_in_file(testspy, "from .models import", "from ~~~PROJNAME~~~.models.mymodel import")
    substitute_in_file(testspy, "from .views import", "from ~~~PROJNAME~~~.views.home import")

    # Copy tests.py to the tests package
    #shutil.copy(os.path.join(os.getcwd(), options.project_name + "/tests.py"), base_dir + "/tests/tests.py")

    # Copy tests to the app
    #tests_dir = os.path.join(os.getcwd(), options.project_name + "/tests")
    #shutil.copytree(base_dir + "/tests", tests_dir)

    # Delete the unnecessary tests.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/tests.py"))

def setup_alembic():
    global base_dir
    global options
    global abs_env_dir
    global abs_root_dir

    initdb = "4f3b93305fe8_initializedb.py"
    initdbpy = base_dir + "/alembic_versions/" + initdb
    substitute_in_file(initdbpy, "~~~PROJNAME~~~", options.project_name)

    seedinitialdata = "1bc0be10afc1_seed_initial_data.py"
    seedinitialdatapy = base_dir + "/alembic_versions/" + seedinitialdata

    shutil.copy(initdbpy, os.path.join(os.getcwd(), options.project_name + "/alembic/versions/" + initdb))
    
    seeddatapath = os.path.join(os.getcwd(), options.project_name + "/alembic/versions/" + seedinitialdata)
    shutil.copy(seedinitialdatapy, seeddatapath)
    substitute_in_file(seeddatapath, "~~~PROJNAME~~~", options.project_name)


#    os.system("../bin/alembic -c development.ini revision --autogenerate -m \"initializedb\"")
    os.system("../bin/alembic -c development.ini upgrade head")

def _get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.
#full_file_paths = get_filepaths("/Users/johnny/Desktop/TEST")

if __name__ == "__main__":
    main()
