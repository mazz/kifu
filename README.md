initpyr
=======
Deploys a pyramid project that includes SQLAlchemy, alembic, gunicorn, supervisor, celery, RabbitMQ, redis(result backend). A python script that is based on the pyramid_alchemy scaffold.

Requirements:
-------------

    * Python 2.7
    * PyYAML libraries

SETUP(Mac OS X)
---------------

Install nginx:

    brew install nginx

Install redis:

    brew install redis

Install rabbitMQ:

    brew install rabbitmq

Edit the nginx.conf file in /usr/local/etc/nginx. Use the checked-in nginx.conf.sample file as a starting point. You can do `nginx -t` at any time to confirm the nginx.conf file is valid.

Launch nginx on port 80:

    sudo chown root /usr/local/opt/nginx/homebrew.mxcl.nginx.plist
    sudo chmod 644 /usr/local/opt/nginx/homebrew.mxcl.nginx.plist
    sudo launchctl load /usr/local/opt/nginx/homebrew.mxcl.nginx.plist

In a terminal window, launch redis-server.

    redis-server

In a terminal window launch rabbitMQ.

    rabbitmq-server

Clone the initpyr repo locally. Run initpyr.py and create a project called `foo`.

    ./initpyr.py -n foo

The script will in a virtual environment:

    * install the Pyramid web framework
    * install the pyramid_alchemy template scaffolding, installing SQLAlchemy
    * install the pyramid_jinja2 template scaffolding
    * install the alembic database migration package, and initialize it
    * install the celery distributed task queue
    * output the necessary changes required to the nginx.conf file to run the foo app
    * install gunicorn
    * install supervisor
    * execute the template pyramid foo webapp as gunicorn processes from supervisor

In another terminal window, cd to path/to/foo_env/foo and initialize celery by doing:

    ../bin/celery worker --app=foo.queue -l debug

Edit nginx.conf file to point to the foo webapp.

Unload and load nginx.

    sudo launchctl unload /usr/local/opt/nginx/homebrew.mxcl.nginx.plist
    sudo launchctl load /usr/local/opt/nginx/homebrew.mxcl.nginx.plist

View the webapp in a web browser by going to http://localhost/

Confirm that celery is queuing tasks to rabbitMQ and storing them in redis by looking at the celery console.

    [2013-11-09 22:35:56,431: INFO/MainProcess] Task foo.queue.tasks.add[2910b3a8-cc4d-46ed-86f5-856316cb2597] succeeded in 0.0907590389252s: 8

Launching in Production Mode
----------------------------

In another terminal window, cd to path/to/foo_env/foo and launch in production mode by doing:
    
    ../bin/supervisord -n -c supervisor.conf

Launching in Development Mode
----------------------------

In another terminal window, cd to path/to/foo_env/foo and launch in development mode by doing:
    
    ../bin/pserve development.ini

