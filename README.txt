You will need the web.py library for running the builtin webserver I included (sudo easy_install web.py)

other dependencies are: urllib2 and csv

./test.py will start the server and the url will be: http://localhost:8080/search/*keyword* (http://localhost:8080/search/backpacks)

The performance is less than optimal because I ended up having to retry with a small 0.01 second wait in order to avoid the 403 forbidden error.
If I had more time I would get around this by caching metadata in a redis cluster or something like that. I also would have used apache or some proper
webserver instead of web.py, but I thought this was best for a test of this sort.