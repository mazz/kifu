#!/usr/bin/env python
import os
import sys
import subprocess
import string
from optparse import OptionParser
import yaml

options = {}

def main():
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="project_name", type="string", help="Name of the new pyramid project.")
    parser.add_option("-d", "--deploy", dest="deploy_gunicorn", action="store_true", help="Deploy with gunicorn when script finishes.")

    (options, args) = parser.parse_args()

    argc = len(sys.argv[1:])
    
    if options.project_name == None:
        options.project_name = "default"

    settings = open("initpyr.yaml", "r")
    print (yaml.load(settings))

    subprocess.call(["virtualenv", options.project_name + "_env"])
    #activate = options.project_name + "_env/bin/activate"
    #print "activate: " + activate
    #subprocess.call(["source", activate])
    os.chdir(options.project_name + "_env")
    subprocess.call(["bin/easy_install", "pyramid"])
    subprocess.call(["bin/pcreate", "-s", "alchemy", options.project_name])
    os.chdir(options.project_name)
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



    #sed  's/^sqlalchemy.url.*/sqlalchemy.url = sqlite:\/\/\/%(here)s\/pets2.sqlite/g' al.ini
    #sed -i '.orig' 's/^sqlalchemy.url.*/sqlalchemy.url = sqlite:\/\/\/%(here)s\/pets2.sqlite/g' al.ini

    #alembicini1_str = "sed -i 's/^sqlalchemy.url.*/sqlalchemy.url = sqlite:\/\/\/%(here)s\/" + options.project_name + ".sqlite/g' alembic.ini"

    alembicini1_str = "awk '{ gsub(/sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname/, \"sqlalchemy.url = sqlite:///%(here)s/" + options.project_name + ".sqlite\"); print}' alembic.ini > /tmp/alembic.ini && mv /tmp/alembic.ini alembic.ini"
    # sed -i 's/^sqlalchemy.url.*/sqlalchemy.url = sqlite:\/\/\/%(here)s\/" + options.project_name + ".sqlite/g' alembic.ini

    os.system(alembicini1_str) 
    #alembicini2_str = "sed -i 's/^script_location.*/script_location = alembic\nversions = alembic\n/g' alembic.ini"

    alembicini2_str = "awk '{ gsub(/script_location.*/,\"script_location = alembic\\\nversions = alembic\\\n\"); print }' alembic.ini > /tmp/alembic.ini && mv /tmp/alembic.ini alembic.ini"

    os.system(alembicini2_str)
    #alembicenv1_str = "sed -i 's/^target_metadata = None.*/from " + options.project_name + ".models import Base\ntarget_metadata = Base.metadata\n/g' alembic/env.py"
    alembicenv1_str = "awk '{ gsub(/target_metadata = None.*/,\"from " + options.project_name + ".models import Base\\\ntarget_metadata = Base.metadata\\\n\"); print }' alembic/env.py > /tmp/env.py && mv /tmp/env.py alembic/env.py"
    os.system(alembicenv1_str)

    os.system("../bin/alembic revision --autogenerate -m \"starting\"")
    os.system("../bin/alembic stamp head")

    #target_metadata = None

    #[alembic]
    #sqlalchemy.url = sqlite:///%(here)s/pets2.sqlite
    #versions=alembic
    #script_location=alembic

    #from pets2.models import Base
    #target_metadata = Base.metadata

    #alembic revision --autogenerate -m "starting"

    os.system("../bin/gunicorn --paster production.ini")

if __name__ == "__main__":
    main()
