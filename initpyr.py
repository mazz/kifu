#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
from optparse import OptionParser
import yaml
import random
import string

options = {}
unix_app_socket = "app.sock"
project_name_placeholder = "~~~PROJNAME~~~"
base_dir = None
env_dir = None

def main():
    global base_dir
    global env_dir
    global options

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

    subprocess.call(["../bin/python", "setup.py", "develop"])

    os.system("../bin/alembic -c development.ini revision --autogenerate -m \"initializedb\"")
    os.system("../bin/alembic -c development.ini upgrade head")

    if options.supervisor_enabled:
        # Install supervisord and run
        os.system("../bin/pip install supervisor")

        # Copy supervisord.conf file to new environment
        shutil.copy(base_dir + "/supervisord.conf", os.getcwd())
        os.system("../bin/supervisord -n -c supervisord.conf")
        output_nginx_help()
    else:
        os.system("../bin/gunicorn --paster production.ini --bind unix:app.sock --workers 4")

def prepend_in_file(filepath, string):
    with file(filepath, 'r') as original: data = original.read()
    with file(filepath, 'w') as modified: modified.write(string + data)

def substitute_in_file(filename, old_string, new_string):
        s=open(filename).read()
        if old_string in s:
                print 'Changing "{old_string}" to "{new_string}" in "{filename}"'.format(**locals())
                s=s.replace(old_string, new_string)
                f=open(filename, 'w')
                f.write(s)
                f.flush()
                f.close()
        else:
                print 'No occurences of "{old_string}" found in "{filename}" '.format(**locals())

def perform_installs():
    global env_dir
    global options

    # Install pyramid_alembic_mako
    subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(["bin/easy_install", "setuptools_git"])
    subprocess.call(["git", "clone", "https://github.com/inklesspen/pyramid_alembic_mako.git"])
    print "env_dir: " + env_dir
    os.chdir(os.path.abspath(os.path.join(env_dir, "pyramid_alembic_mako")))
    os.system("../bin/pip install .")

    os.chdir(env_dir)
    subprocess.call(["bin/pcreate", "-s", "alembic_mako", options.project_name])

    # Install dependencies in requirements.txt
    requirements = os.path.join(base_dir, "requirements.txt")
    os.system("bin/pip install -r " + requirements)

def setup_maininitpy():
    templateinclude = ("config = Configurator(settings=settings)\n"
    "    config.include(\"pyramid_mako\")")
    maininitpy = os.path.join(os.getcwd(), options.project_name + "/__init__.py")
    substitute_in_file(maininitpy, "config = Configurator(settings=settings)", templateinclude)
    # Tweak the main __init__.py to use the project name and correct models path
    substitute_in_file(maininitpy, "from .models import (", "from ~~~PROJNAME~~~.models import (")

    # Add os.path imports to __init__.py
    mainimports = ("from os.path import abspath\n"
    "from os.path import dirname\n"
    "\n"
    "from pyramid.authentication import AuthTktAuthenticationPolicy\n"
    "from pyramid.authorization import ACLAuthorizationPolicy\n"
    "\n"
    "from ~~~PROJNAME~~~.lib.access import RequestWithUserAttribute\n"
    "from ~~~PROJNAME~~~.models.auth import UserMgr\n"
    "\n"
    "from pyramid.security import Allow\n"
    "from pyramid.security import Everyone\n"
    "from pyramid.security import ALL_PERMISSIONS\n"
    "\n"
    "class RootFactory(object):\n"
    "    __acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]\n"
    "\n"
    "    def __init__(self, request):\n"
    "        if request.matchdict:\n"
    "            self.__dict__.update(request.matchdict)\n"
    "\n"
    "\n")

    prepend_in_file(maininitpy, mainimports)

    userauth = ("def main(global_config, **settings):\n"
        "\n"
        "    settings[\"app_root\"] = abspath(dirname(dirname(__file__)))\n"
        "\n"
        "    authn_policy = AuthTktAuthenticationPolicy(\n"
        "       settings.get(\"auth.secret\"),\n"
        "       callback=UserMgr.auth_groupfinder)\n"
        "    authz_policy = ACLAuthorizationPolicy()\n"
        "\n"
        "    config = Configurator(settings=settings,\n"
        "        root_factory=\"~~~PROJNAME~~~.RootFactory\",\n"
        "        authentication_policy=authn_policy,\n"
        "        authorization_policy=authz_policy)\n"
        "\n"
        "\n"
        "    config.set_request_factory(RequestWithUserAttribute)\n")

    substitute_in_file(maininitpy, "def main(global_config, **settings):", userauth)

    # Replace ~~~PROJNAME~~~ placeholders in the __init__.py code
    substitute_in_file(maininitpy, "~~~PROJNAME~~~", options.project_name)

def setup_dotini():
    developmentini = os.path.abspath(os.path.join(os.getcwd(), "development.ini"))
    productionini = os.path.join(os.getcwd(), "production.ini")

    # Add template if it is in the yaml file
    #if settings["template"] != None:        
    
    substitute_in_file(developmentini, "pyramid.includes =", "pyramid.includes =\n    pyramid_mako")
    substitute_in_file(productionini, "pyramid.includes =", "pyramid.includes =\n    pyramid_mako")
    authsecret_orig = "sqlalchemy.url = sqlite:///%(here)s/" + options.project_name + ".sqlite"
    authsecret_subst = authsecret_orig + "\n\nauth.secret=PLEASECHANGEME"
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

    # Delete the unnecessary models.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/models.py"))

    # copy lib to project
    lib_dir = os.path.join(os.getcwd(), options.project_name + "/lib")
    shutil.copytree(base_dir + "/lib", lib_dir)

    # Replace ~~~PROJNAME~~~ placeholders in the lib code
    accesspy = os.path.join(lib_dir, "access.py")
    substitute_in_file(accesspy, "~~~PROJNAME~~~", options.project_name)

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

def output_nginx_help():
    global options
    global unix_app_socket

    # Help text for configuring nginx
    print ""
    print "add to nginx http {} section:"
    print "upstream "+ options.project_name + "-site {"
    print "     server unix://" + os.path.abspath(unix_app_socket) + " fail_timeout=0;"
    print "}"
    print ""
    print "add to nginx server {} section:"
    print "server {"
    print ""
    print "    # optional ssl configuration"
    print ""
    print "    #listen 443 ssl;"
    print "    #ssl_certificate /path/to/ssl/pem_file;"
    print "    #ssl_certificate_key /path/to/ssl/certificate_key;"
    print ""
    print "    # end of optional ssl configuration"
    print "    listen 80;"
    print "    server_name _;"
    print ""
    print "    access_log  " + os.getcwd() + "/access.log;"
    print "    error_log   " + os.getcwd() + "/error.log;"
    print "" 
    print "    location /static/ {"
    print "        root                    " + os.getcwd() + "/" + options.project_name + "/;"
    print "        expires                 30d;"
    print "        add_header              Cache-Control public;"
    print "        access_log              off;"
    print "    }"
    print ""
    print ""
    print "    location / {"
    print "        proxy_set_header        Host $http_host;"
    print "        proxy_set_header        X-Real-IP $remote_addr;"
    print "        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;"
    print "        proxy_set_header        X-Forwarded-Proto $scheme;"
    print ""
    print "        client_max_body_size    10m;"
    print "        client_body_buffer_size 128k;"
    print "        proxy_connect_timeout   60s;"
    print "        proxy_send_timeout      90s;"
    print "        proxy_read_timeout      90s;"
    print "        proxy_buffering         off;"
    print "        proxy_temp_file_write_size 64k;"
    print "        proxy_pass http://" + options.project_name + "-site;"
    print "        proxy_redirect          off;"
    print "    }"
    print "}"

if __name__ == "__main__":
    main()
