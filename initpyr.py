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

def main():
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

    settingsdict = open(base_dir + "/initpyr.yaml", "r")
    settings = (yaml.load(settingsdict))

    os.chdir(absolute_deploydir)
    
    subprocess.call(["virtualenv", options.project_name + "_env"])
    os.chdir(options.project_name + "_env")

    subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(["bin/pcreate", "-s", "alchemy", options.project_name])

    if settings["template"] != "default":
        subprocess.call(["bin/pip", "install", settings["template"]])

    os.chdir(options.project_name)

    maininitpy = os.path.join(os.getcwd(), options.project_name + "/__init__.py")
    developmentini = os.path.abspath(os.path.join(os.getcwd(), "development.ini"))
    productionini = os.path.join(os.getcwd(), "production.ini")

    # Add jinja2 if it is in the yaml file
    if settings["template"] == "pyramid_jinja2":
        jinjarenderer = ("config = Configurator(settings=settings)\\\n"
        "    config.add_renderer(\\\".html\\\", \\\"pyramid_jinja2.renderer_factory\\\")")
        substitute_in_file(maininitpy, "config = Configurator\(settings=settings\)", jinjarenderer)
        
        jinjainclude = ("config = Configurator(settings=settings)\\\n"
        "    config.include(\\\"pyramid_jinja2\\\")")
        substitute_in_file(maininitpy, "config = Configurator\(settings=settings\)", jinjainclude)
        substitute_in_file(developmentini, "pyramid.includes =", "pyramid.includes =\\\n    pyramid_jinja2")
        substitute_in_file(productionini, "pyramid.includes =", "pyramid.includes =\\\n    pyramid_jinja2")

    # Copy Celery-related files to the app
    celery_dir = os.path.join(os.getcwd(), options.project_name + "/queue")
    shutil.copytree(base_dir + "/queue", celery_dir)

    # Copy models.py to the models package and rename it mymodel.py
    shutil.copy(os.path.join(os.getcwd(), options.project_name + "/models.py"), base_dir + "/models/mymodel.py")

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

    substitute_in_file(initializedbpy, "from ..models import \(", "from ~~~PROJNAME~~~.models.mymodel import \(")

    # Replace ~~~PROJNAME~~~ placeholders in the initializedb.py code
    substitute_in_file(initializedbpy, "~~~PROJNAME~~~", options.project_name)

    # Tweak the views.py to use the project name and correct models path
    viewspy = os.path.join(os.getcwd(), options.project_name + "/views.py")

    substitute_in_file(viewspy, "from .models import", "from ~~~PROJNAME~~~.models.mymodel import")
    substitute_in_file(viewspy, "templates\/mytemplate.pt", "~~~PROJNAME~~~:templates/mytemplate.pt")

    # Queue a trivial celery task when the default view loads
    prepend_in_file(viewspy, "from ~~~PROJNAME~~~.queue import tasks")
    substitute_in_file(viewspy, "~~~PROJNAME~~~", options.project_name)
    substitute_in_file(viewspy, "def my_view\(request\):", "def my_view\(request\):\\\n    tasks.add.delay\(5,5\)")

    # Copy views.py to the views package and rename it home.py
    shutil.copy(os.path.join(os.getcwd(), options.project_name + "/views.py"), base_dir + "/views/home.py")

    # Copy views to the app
    views_dir = os.path.join(os.getcwd(), options.project_name + "/views")
    shutil.copytree(base_dir + "/views", views_dir)

    # Delete the unnecessary views.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/views.py"))

    # Tweak the main __init__.py to use the project name and correct models path
    substitute_in_file(maininitpy, "from .models import \(", "from ~~~PROJNAME~~~.models.mymodel import \(")

    # Add os.path imports to __init__.py
    mainimports = ("from os.path import abspath\\\n"
    "from os.path import dirname\\\n"
    "\\\n"
    "from pyramid.authentication import AuthTktAuthenticationPolicy\\\n"
    "from pyramid.authorization import ACLAuthorizationPolicy\\\n"
    "\\\n"
    "from ~~~PROJNAME~~~.lib.access import RequestWithUserAttribute\\\n"
    "from ~~~PROJNAME~~~.models.auth import UserMgr\\\n"
    "\\\n"
    "from pyramid.security import Allow\\\n"
    "from pyramid.security import Everyone\\\n"
    "from pyramid.security import ALL_PERMISSIONS\\\n"
    "\\\n"
    "class RootFactory(object):\\\n"
    "    __acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]\\\n"
    "\\\n"
    "    def __init__(self, request):\\\n"
    "        if request.matchdict:\\\n"
    "            self.__dict__.update(request.matchdict)\\\n"
    "\\\n"
    "\\\n")

    prepend_in_file(maininitpy, mainimports)

    userauth = ("def main\(global_config, \*\*settings\)\:\\\n"
        "\\\n"
        "    settings\[\\\"app_root\\\"\] = abspath\(dirname\(dirname\(__file__\)\)\)\\\n"
        "\\\n"
        "    authn_policy = AuthTktAuthenticationPolicy(\\\n"
        "       settings.get(\\\"auth.secret\\\"),\\\n"
        "       callback=UserMgr.auth_groupfinder)\\\n"
        "    authz_policy = ACLAuthorizationPolicy()\\\n"
        "\\\n"
        "    config = Configurator(settings=settings,\\\n"
        "        root_factory=\\\"~~~PROJNAME~~~.RootFactory\\\",\\\n"
        "        authentication_policy=authn_policy,\\\n"
        "        authorization_policy=authz_policy)\\\n"
        "\\\n"
        "\\\n"
        "    config.set_request_factory(RequestWithUserAttribute)\\\n")

    substitute_in_file(maininitpy, "def main\(global_config, \*\*settings\)\:", userauth)

    # Replace ~~~PROJNAME~~~ placeholders in the __init__.py code
    substitute_in_file(maininitpy, "~~~PROJNAME~~~", options.project_name)

    authsecret_orig = "sqlalchemy.url = sqlite:\/\/\/%\(here\)s\/" + options.project_name + ".sqlite"
    authsecret_subst = authsecret_orig + "\\\n\\\nauth.secret=PLEASECHANGEME"
    substitute_in_file(developmentini, authsecret_orig, authsecret_subst)
    substitute_in_file(productionini, authsecret_orig, authsecret_subst)

    # Tweak the tests.py to use the project name and correct models path
    testspy = os.path.join(os.getcwd(), options.project_name + "/tests.py")

    substitute_in_file(testspy, "from .models import DBSession", "from ~~~PROJNAME~~~.models.mymodel import DBSession")
    substitute_in_file(testspy, "from .models import", "from ~~~PROJNAME~~~.models.mymodel import")
    substitute_in_file(testspy, "from .views import", "from ~~~PROJNAME~~~.views.home import")
    substitute_in_file(testspy, "~~~PROJNAME~~~", options.project_name)

    # Copy tests.py to the tests package
    shutil.copy(os.path.join(os.getcwd(), options.project_name + "/tests.py"), base_dir + "/tests/tests.py")

    # Copy tests to the app
    tests_dir = os.path.join(os.getcwd(), options.project_name + "/tests")
    shutil.copytree(base_dir + "/tests", tests_dir)

    # Delete the unnecessary tests.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/tests.py"))

    # Install dependencies in requirements.txt
    requirements = os.path.join(base_dir, "requirements.txt")
    os.system("../bin/pip install -r " + requirements)

    subprocess.call(["../bin/python", "setup.py", "develop"])
    subprocess.call(["../bin/initialize_" + options.project_name + "_db", "development.ini"])
    subprocess.call(["../bin/alembic", "init", "alembic"])

    alembicini = os.path.join(os.getcwd(), "alembic.ini")

    substitute_in_file(alembicini, "sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname", "sqlalchemy.url = sqlite:///%(here)s/" + options.project_name + ".sqlite")
    substitute_in_file(alembicini, "script_location.*", "script_location = alembic\\\nversions = alembic\\\n")
    substitute_in_file(alembicini, "target_metadata = None.*", "from " + options.project_name + ".models import Base\\\ntarget_metadata = Base.metadata\\\n")

    os.system("../bin/alembic revision --autogenerate -m \"starting\"")
    os.system("../bin/alembic stamp head")

    substitute_in_file(productionini, "\[server:main\]", "[server:main]\\\nunix_socket = %(here)s/" + unix_app_socket + "\\\n") 

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

    if options.supervisor_enabled:
        # Install supervisord and run
        os.system("../bin/pip install supervisor")

        # Copy supervisord.conf file to new environment
        shutil.copy(base_dir + "/supervisord.conf", os.getcwd())
        os.system("../bin/supervisord -n -c supervisord.conf")
    else:
        os.system("../bin/gunicorn --paster production.ini --bind unix:app.sock --workers 4")

def prepend_in_file(filepath, string):
    tempfile = id_generator()
    prepend_call = "awk 'BEGIN{print\"" + string + "\"}1' " + filepath + " > /tmp/" +tempfile+ " && mv /tmp/" +tempfile+ " " + filepath
    os.system(prepend_call)

def substitute_in_file(filepath, original, substitution):
    tempfile = id_generator()
    substitution_call = "awk '{ gsub(/" + original + "/, \"" + substitution + "\"); print }' " + filepath + " > /tmp/" + tempfile + " && mv /tmp/" + tempfile + " " + filepath + ""
    os.system(substitution_call)

def id_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for x in range(size))

if __name__ == "__main__":
    main()
