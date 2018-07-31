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

In this sample app, the task `update_data` (in `tasks.py`) creates a dataframe with sample data, then saves it in redis so that the Dash app, running on a separate process (or a separate container), can have access to it, and read it.

Using the function `setup_periodic_tasks` (also in `tasks.py`), we add the task above, `update_data`, to the list of periodic tasks, with an interval of 15, so this task runs every 15 seconds.

## Deployment

In order to do this, you need to run:

### Locally:

* A Redis instance, a simple way to do this, if you have docker locally, is to run a Redis container:
`docker run --name local-redis -d redis`

Then:
`docker inspect local-redis | grep IPAddress` to get your redis instance's IP address

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

### On your On-Prem server

In order to have this setup when deploying your dash app to your Plotly On-Prem server, your `Procfile` has to execute these three processes (`celery worker`, `celery beat` and the dash app)

In order to run Celery tasks On your Plotly On-Prem server, worker has to be running and linked to your dash app. To do this, scale
up your app's "worker" processes:

```
ssh dokku@YOUR_DASH_SERVER ps:scale APP-NAME worker=1
```

Just like in the local setup, you need a Redis instance to be running and to be linked to your Dash App:

To create and link a Redis database in Dash On Premise:

```
ssh dokku@YOUR_DASH_SERVER redis:create SERVICE-NAME
ssh dokku@YOUR_DASH_SERVER redis:link SERVICE-NAME APP-NAME
```

If you want to link an existing redis instance/service, you can simply use the second command, using the SERVICE-NAME of the existing redis instance.

In the commands above, replace:
* `YOUR_DASH_SERVER` with the name of your Dash server (same as when you run `git remote add`)
* `SERVICE-NAME` with the name you want for your Redis service
* `APP-NAME` with the name of your app (as specified in the Dash App Manager).

