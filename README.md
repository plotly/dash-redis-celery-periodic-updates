# Dash Redis Demo

This app demonstrates how to:

* Connect to a [Redis](https://redis.io) instance
from [Dash](https://plot.ly/dash).

* Use [Celery](http://docs.celeryproject.org/en/latest/getting-started/introduction.html) for asynchronous (periodic or user-triggered) tasks.

## Redis

It works out of the box with the Redis server built in to
[Dash On Premise](https://plot.ly/products/on-premise/) but could be adapted
to work with other servers such as
[Heroku Redis](https://elements.heroku.com/addons/heroku-redis) or your
local Redis server.

For debugging convenince, we install the
[redis-tools](https://packages.ubuntu.com/trusty/database/redis-tools)
package, which offers the `redis-cli` command. This can be removed
for faster app push times.

To enable Redis in Dash On Premise navigate to the settings page of the Server Manager. Under **Special Options & Customizations** select **Enable Dash Customizations** and then select **Enable Redis Databases for Dash Apps**.

## Celery

This app also includes the Celery task queue and a sample periodic update task. (More information on Celery Periodic Tasks [here](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html))

In this sample app, the task `update_data` (in `tasks.py`) creates a dataframe with sample data, then saves it in Redis so that the Dash app, running on a separate process (or a separate container), can have access to it, and read it.

Using the function `setup_periodic_tasks` (also in `tasks.py`), we add the task above, `update_data`, to the list of periodic tasks, with an interval of 15, so this task runs every 15 seconds.

## Deployment

In order to do this, you need to run:

### Locally (MacOS/Linux):

* A Redis instance, a simple way to do this, if you have docker locally, is to run a Redis container:
`docker run --name local-redis -d redis`

Then:
`docker inspect local-redis | grep IPAddress` to get your Redis instance's IP address

If you don't have docker, alternatively, see the Redis documentation: https://redis.io/documentation to download Redis and set up a local instance.

The next commands need to be running from the root of your Dash App (Where the files `app.py` and `tasks.py` are)

* The scheduler:
`REDIS_URL=redis://<your-redis-instance-ip>:6379 celery -A tasks beat --loglevel=DEBUG`

* The worker that will actually run the tasks:
`REDIS_URL=redis://<your-redis-instance-ip>:6379 celery -A tasks worker --loglevel=DEBUG`

The two command above can be shortened into only one command with the `--beat` tag as follows:
`REDIS_URL=redis://<your-redis-instance-ip>:6379 celery -A tasks worker --beat --loglevel=DEBUG`
But please only do this in development, not in a production environment.

* The dash app:
`REDIS_URL=redis://<your-redis-instance-ip>:6379 python app.py`

### Locally (Windows):
Redis is not optimized to work with Windows, but it is possible to use it. 

#### Running the Redis-Server
1. Download the Redis MSI installer for Windows from https://github.com/MicrosoftArchive/redis/releases & run the MSI installer.

2. Install Redis Python Client with `pip install redis`. 
Note: Originally I had used version `2.10.6` which gave a lot of errors. Upgrading to version `3.2.1` fixed these issues. For more information about the Python client go here: https://redislabs.com/lp/python-redis/

3. Open the cmd and go to the root directory of Redis. Run `redis-server` in cmd. If you get an error check the troubleshooting portion below.  

#### Runing the Redis & Celery Instance
**Note: Ensure you're running the below commands in a terminal such as Git Bash or Cygwin**
* The Redis db (run in root of Redis folder or have in Windows ENV variables):
`redis-server`

* The scheduler:
`REDIS_URL=redis://<your-redis-instance-ip>:6379 celery -A tasks beat --loglevel=DEBUG`

* The worker that will actually run the tasks (ensure you have `gevent` -> `pip install gevent`):
`REDIS_URL=redis://<your-redis-instance-ip>:6379 celery -A tasks worker --loglevel=DEBUG info -P gevent`

* The dash app:
`REDIS_URL=redis://<your-redis-instance-ip>:6379 python app.py`

At the end of it you will have four terminals open in total.

#### Troubleshooting (Windows)
If you see the error: `Can't bind TCP listener *:6379 using Redis on Windows`
Follow these steps: 
1. `cd` to the bin (Ex: `directory of Redis, and run
2. `redis-cli`
3. `shutdown`
4. `exit`
5. open another cmd window, cd to the root directory of your Redis installation, and run in cmd `redis-server`.
More information on this error here: https://stackoverflow.com/questions/31769097/cant-bind-tcp-listener-6379-using-redis-on-windows

### On your On-Prem server

In order to have this setup when deploying your dash app to your Dash Deployment Server, your `Procfile` has to execute these three processes (`celery worker`, `celery beat` and the dash app)

In order to run Celery tasks On your Dash Deployment Server, your processes workers have to be running and linked to your dash app. To do this, scale up your app's workers processes (Using the names your have in your `Procfile`) - Note that this command is not necessary if you have a `DOKKU_SCALE` file that reflects how many workers are assigned to each process, like in this repository:

```
ssh dokku@YOUR_DASH_SERVER ps:scale APP-NAME worker-default=1 worker-beat=1
```

Just like in the local setup, you need a Redis instance to be running and to be linked to your Dash App:

To create and link a Redis database in Dash On Premise:

```
ssh dokku@YOUR_DASH_SERVER redis:create SERVICE-NAME
ssh dokku@YOUR_DASH_SERVER redis:link SERVICE-NAME APP-NAME
```

If you want to link an existing Redis instance/service, you can simply use the second command, using the SERVICE-NAME of the existing Redis instance.

In the commands above, replace:
* `YOUR_DASH_SERVER` with the name of your Dash server (same as when you run `git remote add`)
* `SERVICE-NAME` with the name you want for your Redis service
* `APP-NAME` with the name of your app (as specified in the Dash App Manager).
