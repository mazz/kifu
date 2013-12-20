initpyr
=======
Deploys a pyramid project that includes SQLAlchemy, alembic, gunicorn, supervisor, celery, RabbitMQ, redis(result backend). A python script that is based on the pyramid_alembic_mako scaffold.

Requirements:
-------------

    * Python 2.7


SETUP(Ubuntu Linux)
-------------------

Update your system:

    sudo apt-get update

Install your compiler:

    sudo apt-get install gcc

Install git:

    sudo apt-get install git

Install virtualenv:

    curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz
    tar zxvf virtualenv-1.10.1.tar.gz
    cd virtualenv-1.10.1/
    sudo python setup.py install

Install pyyaml:

    curl -O http://pyyaml.org/download/pyyaml/PyYAML-3.10.tar.gz
    tar zxvf PyYAML-3.10.tar.gz
    cd PyYAML-3.10.tar.gz/
    sudo python setup.py install

Install Python headers:

    sudo apt-get install python-dev

Install bcrypt dependencies:

    sudo apt-get install libffi-dev
    git clone https://github.com/wcdolphin/python-bcrypt.git
    sudo python setup.py install

Install linuxbrew

    sudo apt-get install build-essential curl git ruby libbz2-dev libexpat-dev

    Add to your .bashrc or .zshrc:
        export PATH="$HOME/.linuxbrew/bin:$PATH"
        export LD_LIBRARY_PATH="$HOME/.linuxbrew/lib:$LD_LIBRARY_PATH"

Install this script:

    git clone https://github.com/mazzaroth/initpyr.git


SETUP(Mac OS X)
---------------

Install developer tools from http://apple.com/developer

Install virtualenv:

    curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz
    tar zxvf virtualenv-1.10.1.tar.gz
    cd virtualenv-1.10.1/
    sudo python setup.py install

Install pyyaml:

    curl -O http://pyyaml.org/download/pyyaml/PyYAML-3.10.tar.gz
    tar zxvf PyYAML-3.10.tar.gz
    cd PyYAML-3.10.tar.gz/
    sudo python setup.py install


Continue Setup(All platforms)
-----------------------------

Install nginx:

    brew install nginx

Install redis:

    brew install redis

Install rabbitMQ:

    brew install rabbitmq

Install msmtp

    brew install msmtp

Configure msmtp
---------------

Create a .msmtprc file in $HOME. Use the checked-in msmtprc.sample file as a starting point.

Configure nginx
---------------

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
    * install the pyramid_alembic_mako template scaffolding, installing SQLAlchemy
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
    
    ../bin/supervisord -n -c supervisord.conf

Launching in Development Mode
----------------------------

In another terminal window, cd to path/to/foo_env/foo and launch in development mode by doing:
    
    ../bin/pserve development.ini

