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

Replace `YOUR_DASH_SERVER` with the name of your Dash server (same as when
you run `git remove add`, `SERVICE-NAME` with the name you want for your
Redis service, and `APP-NAME` with the name of your app (as specified in
the Dash App Manager).