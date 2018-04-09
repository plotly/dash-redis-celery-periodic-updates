# Dash Redis Demo

This app demonstrates how to connect to a [Redis](https://redis.io) database
from [Dash](https://plot.ly/dash).

It works out of the box with the Redis server built in to
[Dash On Premise](https://plot.ly/products/on-premise/) but could be adapted
to work with other servers such as
[Heroku Redis](https://elements.heroku.com/addons/heroku-redis) or your
local Redis server.

For debugging convenince, we install the
[redis-tools](https://packages.ubuntu.com/trusty/database/redis-tools)
package, which offers the `redis-cli` command. This can be removed
for faster app push times.

To create and link a Redis database in Dash On Premise:

```
ssh dokku@YOUR_DASH_SERVER redis:create SERVICE-NAME
ssh dokku@YOUR_DASH_SERVER redis:link SERVICE-NAME APP-NAME
```

In the commands above, replace:
* `YOUR_DASH_SERVER` with the name of your Dash server (same as when you run `git remote add`)
* `SERVICE-NAME` with the name you want for your Redis service
* `APP-NAME` with the name of your app (as specified in the Dash App Manager).

## Celery

This app also includes the [Celery](http://docs.celeryproject.org/en/latest/getting-started/introduction.html)
task queue and a sample task.

Clicking the **Run "Hello" task** button runs the task asynchronously. The
task sleeps for 10 seconds then writes the current date and time to a file.

In order to run Celery tasks, a broker needs to be run. To do this, scale
up your app's "worker" process after pushing it:

```
ssh dokku@YOUR_DASH_SERVER ps:scale APP-NAME worker=1
```

As above, replace `APP-NAME` with the name of your app.

To verify that the broker is working correctly, check your app's logs after
clicking the button a few times:

```
ssh dokku@YOUR_DASH_SERVER logs APP-NAME
```

Tasks should show up in the logs when they are submitted (in other words
when "Hello" is clicked), and then the task should complete about 10 seconds
later.