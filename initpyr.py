#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
from optparse import OptionParser
import yaml



options = {}
unix_app_socket = "app.sock"

def main():
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="project_name", type="string", help="Name of the new pyramid project.")
    parser.add_option("-d", "--deploy", dest="deploy_dir", type="string", help="Deploy base directory of webapp.")
    #parser.add_option("-t", "--template", dest="template", type="string", help="Override Chameleon with this template.")

    (options, args) = parser.parse_args()

    argc = len(sys.argv[1:])

    base_dir = os.getcwd();
    
    if options.project_name == None:
        options.project_name = "default"

    if options.deploy_dir == None:
        options.deploy_dir = base_dir

    absolute_deploydir = os.path.abspath(options.deploy_dir)

    settings = open(base_dir + "/initpyr.yaml", "r")
    defaults = (yaml.load(settings))

    os.chdir(absolute_deploydir)
    
    subprocess.call(["virtualenv", options.project_name + "_env"])
    #activate = options.project_name + "_env/bin/activate"
    #print "activate: " + activate
    #subprocess.call(["source", activate])
    os.chdir(options.project_name + "_env")

    if defaults["template"] != "default":
        subprocess.call(["bin/easy_install", defaults["template"]])

    subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(["bin/pcreate", "-s", "alchemy", options.project_name])
    os.chdir(options.project_name)

    if defaults["template"] == "pyramid_jinja2":
        #awk 'BEGIN{print""}1' data.txt
        initpy_importjinja2 = "awk 'BEGIN{print\"import pyramid_jinja2\"}1' default/__init__.py > /tmp/__init__.py && mv /tmp/__init__.py default/__init__.py"
        os.system(initpy_importjinja2)

        initpy_jinjarenderer = "awk '{ gsub(/config = Configurator\(settings=settings\)/, \"config = Configurator(settings=settings)\\\n    config.add_renderer(\\\".html\\\", \\\"pyramid_jinja2.renderer_factory\\\")\"); print }' default/__init__.py > /tmp/__init__.py && mv /tmp/__init__.py default/__init__.py"
        os.system(initpy_jinjarenderer)
        
        initpy_jinjainclude = "awk '{ gsub(/config = Configurator\(settings=settings\)/, \"config = Configurator(settings=settings)\\\n    config.include(\\\"pyramid_jinja2\\\")\"); print }' default/__init__.py > /tmp/__init__.py && mv /tmp/__init__.py default/__init__.py"
        os.system(initpy_jinjainclude)

        developmentini_jinja2 = "awk '{ gsub(/pyramid.includes =/, \"pyramid.includes =\\\n    pyramid_jinja2\\\n\"); print }' development.ini > /tmp/development.ini && mv /tmp/development.ini development.ini"
        os.system(developmentini_jinja2)   

        productionini_jinja2 = "awk '{ gsub(/pyramid.includes =/, \"pyramid.includes =\\\n    pyramid_jinja2\\\n\"); print }' production.ini > /tmp/production.ini && mv /tmp/production.ini production.ini"
        os.system(productionini_jinja2)   


    subprocess.call(["../bin/python", "setup.py", "develop"])
    subprocess.call(["../bin/initialize_" + options.project_name + "_db", "development.ini"])
    
    # install gunicorn
    subprocess.call(["../bin/easy_install", "-U", "gunicorn"])

    # Install alembic
    subprocess.call(["../bin/pip", "install", "alembic"])
    subprocess.call(["../bin/alembic", "init", "alembic"])

    subprocess.call(["../bin/alembic", "init", "alembic"])

    #setup.py
    #'pyramid_mako',
    #'psycopg2',

    #../bin/python setup.py develop

    # alembic.ini
    #sqlalchemy.url = sqlite:///%(here)s/pets2.sqlite
    #versions = alembic

    #alembic/env.py
    #from pets2.models import Base
    #target_metadata = Base.metadata

    #../bin/alembic revision --autogenerate -m "starting"
    #../bin/alembic stamp head

    #__init__.py
    #config.include('pyramid_jinja2')

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


    # Install supervisord and run
    os.system("../bin/pip install supervisor")

    # Copy supervisord.conf file to new environment
    shutil.copy(base_dir + "/supervisord.conf", os.getcwd())

    os.system("../bin/supervisord -n -c supervisord.conf")


if __name__ == "__main__":
    main()
