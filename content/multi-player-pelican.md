Title: Multi-player pelican
Date: 2015-04-14 21:09
Tags: python, pelican, meta

### Preamble

To replace the wordpress [Certified Edible Dinosaurs](http://ced.pwned.systems/) website with a pelican based site, we needed an infrastructure where multiple persons could edit not only the content, but also the settings and the theme of the pelican install. Since we don't mind having everything out in the open, we decided not to mind storing the entire pelican directory (minus the cache and output folders) on GitHub. We're a small team and we trust eachother so allowing each member to push to the repository and having a VPS automatically build the final website is not a problem.

### The set up

So after re-creating the original site using pelican and migrating all the content, I pushed everything to [GitHub](https://github.com/edibledinos/ced.pwned.systems). Now we needed a way to automatically update the website when somebody pushes to the repository. I came across [flask-hookserver](https://pypi.python.org/pypi/flask-hookserver) which allows you to very easily handle GitHub webhooks. I decided to to create a small service that listens for push events and then calls a shell script which will further handle setting up or updating the pelican install and build the website. This service will be a WSGI service that can be hosted by *uwsgi*, *gunicorn* or any other WSGI server.

### The environment

First, let's create a user that will host all the pelican sites I want to publish this way and create a virtual environment that will host the webhook service:

    # useradd -mU pelican
    # su - pelican
    $ virtualenv webhook
    $ source webhook/bin/activate
    (webhook)$ pip install flask-hookserver
    (webhook)$ mkdir sites

### Handling events

Next we'll create the service that will handle the GitHub webhook events.

    from hookserver import HookServer
    import subprocess
    import os

    VALID_OWNERS = ['username1', 'username2']
    home = os.path.dirname(__file__)
    update_script = os.path.join(home, 'update.sh')

    app = HookServer(__name__, b'SuperSecretSecret', 1)

    @app.hook('ping')
    def ping(data, guid):
	    return 'pong'

    @app.hook('push')
    def push(data, guid):
        if not data['repository']['owner']['name'] in VALID_OWNERS:
            raise RuntimeError('Go away, I don\'t trust you.')
        subprocess.check_call([
            update_script,
            data['repository']['full_name'],
            data['repository']['clone_url'],
        ])
        return ''
    
    if __name__ == '__main__':
        app.run()

When this script receives a push event from GitHub, *flask-hookserver* will first verify the originating IP address to see if the event really came from GitHub. It will also check the signature of the event which implies a check of the secret. The script will then check if the owner of the repository being pushed is trusted. If all these conditions are met, it will call the *update.sh* script which resides in the same directory as this script with two parameters: the full name of the repository (*username/repository*) and the URL that can be used to clone the repository.

### Pulling some strings

Let's create a script that will create or update the repositories and build the sites. Save it as *update.sh* in the same directory as the script you created in the previous step.

    #! /bin/bash

    error=0
    if [ -z "$1" ]; then error=1; fi
    if [ -z "$2" ]; then error=1; fi
    if [ $error == 1 ]; then
        echo "Syntax: $0 <repository> <git url>"
        exit 1
    fi

    SITE_DIR="sites/$1"

    fail() {
        rm -rf "$SITE_DIR"
        exit 1
    }
    if [ ! -d "$SITE_DIR" ]; then
        virtualenv "$SITE_DIR" || fail
        cd "$SITE_DIR" || fail
        git clone "$2" site || fail
        cd site || fail
    else
        cd "$SITE_DIR/site" || exit 1
        git fetch origin || exit 1
        git reset --hard origin/master || exit 1
    fi

    source ../bin/activate || exit 1
    pip install -r requirements.txt || exit 1
    pelican -s publishconf.py -o ../public_html || exit 1

The script first checks if it is provided enough arguments and then checks if the destination directory (*sites/owner/repository*) already exists. If it doesn't exist, it and a python virtual environment are created and the repository is cloned. If the destination directory does exist, it updates the clone. It uses `git reset --hard` to make sure that even if someone forces a *non-fast-forward* push to GitHub, the local repository will be able to cope.

Once the repository is set up or updated, it activates the site's very own virtual environment, makes sure the dependencies are up to date and builds the final site to *../public_html* using pelican and the provided publishing configuration.

### Serving it all up

Now, start the webservice. I'll leave that as an excercise to you, the reader. I use *uwsgi* which is started by *supervisor* and connected to the outside world using *nginx*. Configure your GitHub webhook (don't forget to enter the same secret as the one you used in the webhook script).

The final step is configuring your webserver to serve the completely static content found in *~pelican/sites/username/repository/public_html*.

### Publishing content

We now have a shiny autodeployment infrastructure for one or more multi-user pelican websites. So... How do we use it?

Start by granting all users you want to allow to publish content read/write access to the repository (either by using teams in an organization or by making them collaborators of the project).

Each user then clones the repository, starts editing and with the proper pulls and pushes will be able to make their content appear on the internet!
