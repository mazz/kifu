#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
from optparse import OptionParser
import yaml

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
    #activate = options.project_name + "_env/bin/activate"
    #print "activate: " + activate
    #subprocess.call(["source", activate])
    os.chdir(options.project_name + "_env")

    subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(["bin/pcreate", "-s", "alchemy", options.project_name])

    if settings["template"] != "default":
        subprocess.call(["bin/easy_install", settings["template"]])

    os.chdir(options.project_name)

    # Add jinja2 if it is in the yaml file
    if settings["template"] == "pyramid_jinja2":
        #awk 'BEGIN{print""}1' data.txt
        initpy_importjinja2 = "awk 'BEGIN{print\"import pyramid_jinja2\"}1' " + options.project_name + "/__init__.py > /tmp/__init__.py && mv /tmp/__init__.py " + options.project_name + "/__init__.py"
        os.system(initpy_importjinja2)

        initpy_jinjarenderer = "awk '{ gsub(/config = Configurator\(settings=settings\)/, \"config = Configurator(settings=settings)\\\n    config.add_renderer(\\\".html\\\", \\\"pyramid_jinja2.renderer_factory\\\")\"); print }' " + options.project_name + "/__init__.py > /tmp/__init__.py && mv /tmp/__init__.py " + options.project_name + "/__init__.py"
        os.system(initpy_jinjarenderer)
        
        initpy_jinjainclude = "awk '{ gsub(/config = Configurator\(settings=settings\)/, \"config = Configurator(settings=settings)\\\n    config.include(\\\"pyramid_jinja2\\\")\"); print }' " + options.project_name + "/__init__.py > /tmp/__init__.py && mv /tmp/__init__.py " + options.project_name + "/__init__.py"
        os.system(initpy_jinjainclude)

        developmentini_jinja2 = "awk '{ gsub(/pyramid.includes =/, \"pyramid.includes =\\\n    pyramid_jinja2\"); print }' development.ini > /tmp/development.ini && mv /tmp/development.ini development.ini"
        os.system(developmentini_jinja2)   

        productionini_jinja2 = "awk '{ gsub(/pyramid.includes =/, \"pyramid.includes =\\\n    pyramid_jinja2\"); print }' production.ini > /tmp/production.ini && mv /tmp/production.ini production.ini"
        os.system(productionini_jinja2)   

    # Setup Celery
    subprocess.call(["../bin/easy_install", "celery"])

    # Copy Celery-related files to the app
    celery_dir = os.path.join(os.getcwd(), options.project_name + "/queue")
    shutil.copytree(base_dir + "/queue", celery_dir)

    # Copy models.py to the models package and rename it mymodel.py
    shutil.copy(os.path.join(os.getcwd(), options.project_name + "/models.py"), base_dir + "/models/mymodel.py")

    # Copy models dir to the app
    models_dir = os.path.join(os.getcwd(), options.project_name + "/models")
    shutil.copytree(base_dir + "/models", models_dir)

    # Delete the unnecessary models.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/models.py"))

    # Replace ~~~PROJNAME~~~ placeholders in the Celery code
    celerypy = os.path.join(celery_dir, "celery.py")
    celerypy_projname = "awk '{ gsub(/~~~PROJNAME~~~/, \"" + options.project_name + "\"); print }' " + celerypy + " > /tmp/celery.py && mv /tmp/celery.py " + celerypy + ""
    os.system(celerypy_projname)

    taskspy = os.path.join(celery_dir, "tasks.py")
    taskspy_projname = "awk '{ gsub(/~~~PROJNAME~~~/, \"" + options.project_name + "\"); print }' " + taskspy + " > /tmp/tasks.py && mv /tmp/tasks.py " + taskspy + ""
    os.system(taskspy_projname)

    # Tweak initialize db script to use replacement model hierarchy
    initializedbpy = os.path.join(os.getcwd(), options.project_name + "/scripts/initializedb.py")
    initializedbpy_modelpath = "awk '{ gsub(/from ..models import \(/, \"from ~~~PROJNAME~~~.models.mymodel import \(\"); print }' " + initializedbpy + " > /tmp/initializedb.py && mv /tmp/initializedb.py " + initializedbpy + ""
    os.system(initializedbpy_modelpath)

    # Replace ~~~PROJNAME~~~ placeholders in the initializedb.py code
    initializedbpy_projname = "awk '{ gsub(/~~~PROJNAME~~~/, \"" + options.project_name + "\"); print }' " + initializedbpy + " > /tmp/initializedb.py && mv /tmp/initializedb.py " + initializedbpy + ""
    os.system(initializedbpy_projname)

    # Tweak the views.py to use the project name and correct models path
    viewspy = os.path.join(os.getcwd(), options.project_name + "/views.py")
    viewspy_modelpath = "awk '{ gsub(/from .models import \(/, \"from ~~~PROJNAME~~~.models.mymodel import \(\"); print }' " + viewspy + " > /tmp/views.py && mv /tmp/views.py " + viewspy + ""
    os.system(viewspy_modelpath)

    viewspy_templatepath = "awk '{ gsub(/templates\/mytemplate.pt/, \"~~~PROJNAME~~~:templates/mytemplate.pt\"); print }' " + viewspy + " > /tmp/views.py && mv /tmp/views.py " + viewspy + ""
    os.system(viewspy_templatepath)

    # Queue a trivial celery task when the default view loads
    viewspy_importcelery = "awk 'BEGIN{print\"from ~~~PROJNAME~~~.queue import tasks\"}1' " + viewspy + " > /tmp/views.py && mv /tmp/views.py " + viewspy + ""
    os.system(viewspy_importcelery)

    viewspy_projname = "awk '{ gsub(/~~~PROJNAME~~~/, \"" + options.project_name + "\"); print }' " + viewspy + " > /tmp/views.py && mv /tmp/views.py " + viewspy + ""
    os.system(viewspy_projname)

    viewspy_celerytask = "awk '{ gsub(/def my_view\(request\):/, \"def my_view\(request\):\\\n    tasks.add.delay\(4,4\)\"); print }' " + viewspy + " > /tmp/views.py && mv /tmp/views.py " + viewspy + ""
    os.system(viewspy_celerytask)       

    # Copy views.py to the views package and rename it home.py
    shutil.copy(os.path.join(os.getcwd(), options.project_name + "/views.py"), base_dir + "/views/home.py")

    # Copy views to the app
    views_dir = os.path.join(os.getcwd(), options.project_name + "/views")
    shutil.copytree(base_dir + "/views", views_dir)

    # Delete the unnecessary views.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/views.py"))

    # Tweak the main __init__.py to use the project name and correct models path
    maininitpy = os.path.join(os.getcwd(), options.project_name + "/__init__.py")
    maininitpy_modelpath = "awk '{ gsub(/from .models import \(/, \"from ~~~PROJNAME~~~.models.mymodel import \(\"); print }' " + maininitpy + " > /tmp/views.py && mv /tmp/views.py " + maininitpy + ""
    os.system(maininitpy_modelpath)

    # Tweak the main __init__.py to use the project name and correct models path
    maininitpy_modelpath = "awk '{ gsub(/from .models import \(/, \"from ~~~PROJNAME~~~.models.mymodel import \(\"); print }' " + maininitpy + " > /tmp/views.py && mv /tmp/views.py " + maininitpy + ""
    os.system(maininitpy_modelpath)

    # Replace ~~~PROJNAME~~~ placeholders in the __init__.py code
    maininitpy_projname = "awk '{ gsub(/~~~PROJNAME~~~/, \"" + options.project_name + "\"); print }' " + maininitpy + " > /tmp/maininit.py && mv /tmp/maininit.py " + maininitpy + ""
    os.system(maininitpy_projname)

    # Tweak the tests.py to use the project name and correct models path

    testspy = os.path.join(os.getcwd(), options.project_name + "/tests.py")
    testspy_modelpath = "awk '{ gsub(/from .models import DBSession/, \"from ~~~PROJNAME~~~.models.mymodel import DBSession\"); print }' " + testspy + " > /tmp/tests.py && mv /tmp/tests.py " + testspy + ""
    os.system(testspy_modelpath)

    testspy_modelpath = "awk '{ gsub(/from .models import/, \"from ~~~PROJNAME~~~.models.mymodel import\"); print }' " + testspy + " > /tmp/tests.py && mv /tmp/tests.py " + testspy + ""
    os.system(testspy_modelpath)

    testspy_viewpath = "awk '{ gsub(/from .views import/, \"from ~~~PROJNAME~~~.views.home import\"); print }' " + testspy + " > /tmp/tests.py && mv /tmp/tests.py " + testspy + ""
    os.system(testspy_viewpath)


    # Replace ~~~PROJNAME~~~ placeholders in the tests.py code
    testspy_projname = "awk '{ gsub(/~~~PROJNAME~~~/, \"" + options.project_name + "\"); print }' " + testspy + " > /tmp/tests.py && mv /tmp/tests.py " + testspy + ""
    os.system(testspy_projname)

    # Copy tests.py to the tests package
    shutil.copy(os.path.join(os.getcwd(), options.project_name + "/tests.py"), base_dir + "/tests/tests.py")

    # Copy tests to the app
    tests_dir = os.path.join(os.getcwd(), options.project_name + "/tests")
    shutil.copytree(base_dir + "/tests", tests_dir)

    # Delete the unnecessary tests.py file
    os.unlink(os.path.join(os.getcwd(), options.project_name + "/tests.py"))

    # Redis is used as a result backend
    subprocess.call(["../bin/pip", "install", "redis"])    

    subprocess.call(["../bin/python", "setup.py", "develop"])
    subprocess.call(["../bin/initialize_" + options.project_name + "_db", "development.ini"])
    
    # install gunicorn
    subprocess.call(["../bin/easy_install", "-U", "gunicorn"])

    # Install alembic
    subprocess.call(["../bin/pip", "install", "alembic"])
    subprocess.call(["../bin/alembic", "init", "alembic"])

    # edit alembic.ini with `sqlalchemy.url = sqlite:///%(here)s/projname.sqlite`
    alembicini1_str = "awk '{ gsub(/sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname/, \"sqlalchemy.url = sqlite:///%(here)s/" + options.project_name + ".sqlite\"); print}' alembic.ini > /tmp/alembic.ini && mv /tmp/alembic.ini alembic.ini"

    os.system(alembicini1_str) 

    # edit alembic.ini from `script_location` to 
    # `script_location = alembic`
    # `versions = alembic`
    alembicini2_str = "awk '{ gsub(/script_location.*/,\"script_location = alembic\\\nversions = alembic\\\n\"); print }' alembic.ini > /tmp/alembic.ini && mv /tmp/alembic.ini alembic.ini"

    os.system(alembicini2_str)
    #alembicenv1_str = "sed -i 's/^target_metadata = None.*/from " + options.project_name + ".models import Base\ntarget_metadata = Base.metadata\n/g' alembic/env.py"

    # edit env.py from `target_metadata = None` to `from projname.models import Base\ntarget_metadata = Base.metadata`
    alembicenv1_str = "awk '{ gsub(/target_metadata = None.*/,\"from " + options.project_name + ".models import Base\\\ntarget_metadata = Base.metadata\\\n\"); print }' alembic/env.py > /tmp/env.py && mv /tmp/env.py alembic/env.py"
    os.system(alembicenv1_str)

    os.system("../bin/alembic revision --autogenerate -m \"starting\"")
    os.system("../bin/alembic stamp head")

    productionini_socket = "awk '{ gsub(/\[server:main\]/, \"[server:main]\\\nunix_socket = %(here)s/" + unix_app_socket + "\\\n\"); print }' production.ini > /tmp/production.ini && mv /tmp/production.ini production.ini"
    os.system(productionini_socket)   
    #unix_socket = %(here)s/app.sock
#    config = Configurator(settings=settings)

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

if __name__ == "__main__":
    main()
