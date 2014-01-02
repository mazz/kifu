#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
from optparse import OptionParser
import yaml
import random
import string
import logging

logger = logging.getLogger('initpyr')
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
env_dir = None
settings = None

def main():
    global base_dir
    global env_dir
    global options
    global settings

    parser = OptionParser()
    parser.add_option("-n", "--name", dest="project_name", type="string", help="Name of the new pyramid project.")
    parser.add_option("-d", "--deploy", dest="deploy_dir", type="string", help="Deploy base directory of webapp.")
    parser.add_option("-s", "--supervisor-enabled", action="store_true", dest="supervisor_enabled", help="Run gunicorn with supervisor.")

    (options, args) = parser.parse_args()

    argc = len(sys.argv[1:])

    base_dir = os.getcwd();
    
    if options.project_name == None:
        options.project_name = "default"

    if options.deploy_dir == None:
        options.deploy_dir = base_dir

    if options.supervisor_enabled == None:
        options.supervisor_enabled = False

    with open('initpyr.yaml') as f:
        settings = yaml.load(f)

    absolute_deploydir = os.path.abspath(options.deploy_dir)
    os.chdir(absolute_deploydir)
    
    subprocess.call(["virtualenv", options.project_name + "_env"])

    env_dir = os.path.abspath(os.path.join(absolute_deploydir, options.project_name + "_env"))
    os.chdir(env_dir)

    perform_installs()

    os.chdir(options.project_name)

    setup_maininitpy()
    setup_dotini()
    setup_packages()
    setup_tests()

    subprocess.call(["../bin/python", "setup.py", "develop"])

    setup_alembic()

    if options.supervisor_enabled:

        output_nginx_help()
        # Install supervisord and run
        os.system("../bin/pip install supervisor")

        # Copy supervisord.conf file to new environment
        shutil.copy(base_dir + "/supervisord.conf", os.getcwd())
        substitute_in_file(os.path.join(os.getcwd(), "supervisord.conf"), "~~~PROJNAME~~~", options.project_name)

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

def perform_installs():
    global env_dir
    global options

    # Install pyramid_alembic_mako
    subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(["bin/easy_install", "setuptools_git"])
    subprocess.call(["git", "clone", "https://github.com/inklesspen/pyramid_alembic_mako.git"])
    os.chdir(os.path.abspath(os.path.join(env_dir, "pyramid_alembic_mako")))
    os.system("../bin/pip install .")

    os.chdir(env_dir)
    subprocess.call(["bin/pcreate", "-s", "alembic_mako", options.project_name])

    subprocess.call(["bin/easy_install", "bcrypt"])
    subprocess.call(["bin/easy_install", "celery"])
    subprocess.call(["bin/easy_install", "decorator"])
    subprocess.call(["bin/easy_install", "gunicorn"])
    subprocess.call(["bin/easy_install", "redis"])
#    subprocess.call(["bin/easy_install", "breadability"])
#    subprocess.call(["bin/easy_install", "lxml"])

    # Install dependencies in requirements.txt
    #requirements = os.path.join(base_dir, "requirements.txt")
    #os.system("bin/pip install -r " + requirements)

def setup_maininitpy():
    global settings

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

    # Replace ~~~PROJNAME~~~ placeholders in the __init__.py code
    substitute_in_file(maininitpy, "~~~PROJNAME~~~", options.project_name)

    # We add routes via routes.py now, so remove this template code
    substitute_in_file(maininitpy, "    config.add_route(\'home\', \'/\')", "")

def setup_dotini():
    developmentini = os.path.abspath(os.path.join(os.getcwd(), "development.ini"))
    productionini = os.path.join(os.getcwd(), "production.ini")

    # Add template if it is in the yaml file
    #if settings["template"] != None:        
    
    substitute_in_file(developmentini, "pyramid.includes =", "pyramid.includes =\n    pyramid_mako")
    substitute_in_file(productionini, "pyramid.includes =", "pyramid.includes =\n    pyramid_mako")
    authsecret_orig = "sqlalchemy.url = sqlite:///%(here)s/" + options.project_name + ".sqlite"
    authsecret_subst = authsecret_orig + "\n\nauth.secret=PLEASECHANGEME\n\nemail.enable=true\nemail.from=change@me.com\nemail.host=sendmail"
    substitute_in_file(developmentini, authsecret_orig, authsecret_subst)
    substitute_in_file(productionini, authsecret_orig, authsecret_subst)
    substitute_in_file(productionini, "[server:main]", "[server:main]\nunix_socket = %(here)s/" + unix_app_socket + "\n") 


def setup_packages():
    global options
    global base_dir
    # Copy Celery-related files to the app
    celery_dir = os.path.join(os.getcwd(), options.project_name + "/queue")
    shutil.copytree(base_dir + "/queue", celery_dir)

    # Copy models.py to the models package and rename it mymodel.py
    #shutil.copy(os.path.join(os.getcwd(), options.project_name + "/models.py"), base_dir + "/models/mymodel.py")

    # Copy models dir to the app
    models_dir = os.path.join(os.getcwd(), options.project_name + "/models")
    shutil.copytree(base_dir + "/models", models_dir)

    # Replace ~~~PROJNAME~~~ placeholders in the auth code
    authpy = os.path.join(models_dir, "auth.py")
    substitute_in_file(authpy, "~~~PROJNAME~~~", options.project_name)

    # Replace ~~~PROJNAME~~~ placeholders in the applog code
    applogpy = os.path.join(models_dir, "applog.py")
    substitute_in_file(applogpy, "~~~PROJNAME~~~", options.project_name)

    # Delete the unnecessary models.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/models.py"))

    ### lib ###

    # copy lib to project
    lib_dir = os.path.join(os.getcwd(), options.project_name + "/lib")
    shutil.copytree(base_dir + "/lib", lib_dir)

    # Replace ~~~PROJNAME~~~ placeholders in the lib code
    accesspy = os.path.join(lib_dir, "access.py")
    substitute_in_file(accesspy, "~~~PROJNAME~~~", options.project_name)

    # Replace ~~~PROJNAME~~~ placeholders in the lib code
    libapplogpy = os.path.join(lib_dir, "applog.py")
    substitute_in_file(libapplogpy, "~~~PROJNAME~~~", options.project_name)

    libreadablepy = os.path.join(lib_dir, "readable.py")
    substitute_in_file(libreadablepy, "~~~PROJNAME~~~", options.project_name)

    ### celery ###

    # Replace ~~~PROJNAME~~~ placeholders in the Celery code
    celerypy = os.path.join(celery_dir, "celery.py")
    substitute_in_file(celerypy, "~~~PROJNAME~~~", options.project_name)

    taskspy = os.path.join(celery_dir, "tasks.py")
    substitute_in_file(taskspy, "~~~PROJNAME~~~", options.project_name)

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
    homepy = os.path.join(views_dir, "home.py")
    substitute_in_file(homepy, "~~~PROJNAME~~~", options.project_name)

    # Delete mymodel.py
    mymodelpy = os.path.join(os.getcwd(), options.project_name + "/models/mymodel.py")
    os.unlink(mymodelpy)

    # Copy over Foundation 5.02 static css/js resources 
    css_dir = os.path.join(os.getcwd(), options.project_name + "/static/css")
    shutil.copytree(base_dir + "/static/css", css_dir)
    img_dir = os.path.join(os.getcwd(), options.project_name + "/static/img")
    shutil.copytree(base_dir + "/static/img", img_dir)
    js_dir = os.path.join(os.getcwd(), options.project_name + "/static/js")
    shutil.copytree(base_dir + "/static/js", js_dir)

    # Copy over templates
    accounts_dir = os.path.join(os.getcwd(), options.project_name + "/templates/accounts")
    shutil.copytree(base_dir + "/templates/accounts", accounts_dir)

    signupmako = base_dir + "/templates/auth/signup.mako"
    substitute_in_file(signupmako, "~~~PROJNAME~~~", options.project_name)

    auth_dir = os.path.join(os.getcwd(), options.project_name + "/templates/auth")
    shutil.copytree(base_dir + "/templates/auth", auth_dir)

    layoutmako = base_dir + "/templates/layout.mako"
    list_usersmako = base_dir + "/templates/list_users.mako"

    # Copy over layout.mako
    shutil.copy(layoutmako, os.path.join(os.getcwd(), options.project_name + "/templates/layout.mako"))
    substitute_in_file(os.path.join(os.getcwd(), options.project_name + "/templates/layout.mako"), "~~~PROJNAME~~~", options.project_name)

    # Copy over list_users.mako
    shutil.copy(list_usersmako, os.path.join(os.getcwd(), options.project_name + "/templates/list_users.mako"))

    # Copy over routes.py
    routespy = base_dir + "/routes.py"
    shutil.copy(routespy, os.path.join(os.getcwd(), options.project_name + "/routes.py"))

    ### views ###

    viewsauthpy = base_dir + "/views/auth.py"

    # Copy over views auth.py
    shutil.copy(viewsauthpy, os.path.join(os.getcwd(), options.project_name + "/views/auth.py"))
    # Replace ~~~PROJNAME~~~ placeholders in the auth code
    substitute_in_file(os.path.join(os.getcwd(), options.project_name + "/views/auth.py"), "~~~PROJNAME~~~", options.project_name)

    viewsaccountspy = base_dir + "/views/accounts.py"

    # Copy over views accounts.py
    shutil.copy(viewsaccountspy, os.path.join(os.getcwd(), options.project_name + "/views/accounts.py"))
    # Replace ~~~PROJNAME~~~ placeholders in the accounts code
    substitute_in_file(os.path.join(os.getcwd(), options.project_name + "/views/accounts.py"), "~~~PROJNAME~~~", options.project_name)

    viewsapipy = base_dir + "/views/api.py"

    # Copy over views api.py
    shutil.copy(viewsapipy, os.path.join(os.getcwd(), options.project_name + "/views/api.py"))
    # Replace ~~~PROJNAME~~~ placeholders in the accounts code
    substitute_in_file(os.path.join(os.getcwd(), options.project_name + "/views/api.py"), "~~~PROJNAME~~~", options.project_name)


def output_nginx_help():
    global options
    global unix_app_socket

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

    # Tweak the tests.py to use the project name and correct models path
    testspy = os.path.join(os.getcwd(), options.project_name + "/tests.py")

    substitute_in_file(testspy, "from .models import DBSession", "from ~~~PROJNAME~~~.models.mymodel import DBSession")
    substitute_in_file(testspy, "from .models import", "from ~~~PROJNAME~~~.models.mymodel import")
    substitute_in_file(testspy, "from .views import", "from ~~~PROJNAME~~~.views.home import")
    substitute_in_file(testspy, "~~~PROJNAME~~~", options.project_name)

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

    initdb = "4f3b93305fe8_initializedb.py"
    initdbpy = base_dir + "/alembic_versions/" + initdb

    seedinitialdata = "1bc0be10afc1_seed_initial_data.py"
    seedinitialdatapy = base_dir + "/alembic_versions/" + seedinitialdata

    shutil.copy(initdbpy, os.path.join(os.getcwd(), options.project_name + "/alembic/versions/" + initdb))
    shutil.copy(seedinitialdatapy, os.path.join(os.getcwd(), options.project_name + "/alembic/versions/" + seedinitialdata))

#    os.system("../bin/alembic -c development.ini revision --autogenerate -m \"initializedb\"")
    os.system("../bin/alembic -c development.ini upgrade head")


if __name__ == "__main__":
    main()
