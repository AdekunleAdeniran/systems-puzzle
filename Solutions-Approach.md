### Solution Approach
After running the codes:
```
docker-compose up -d db
docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
docker-compose up -d
```
I tried using  ```curl localhost:8080``` to check if it was up and running and I got ```curl: (7) Failed to connect to localhost port 8080: Connection refused```. My first instinct was to check the error logs

Before I discovered I could use the Docker extension on VS-CODE to degub much easier, I was using ```docker ps``` to identify the individual containers running and used ```docker logs <container id>``` to check for all logs in each container. 

This didn't give any error messages to work with so i decided to review the files one by one starting with the docker-compose.yml. 

I also reviewed docker-compose documentation where I discovered that the nginx port mapping should be mapping the 8080 of local host to port 80 of the container ```8080:80``` but instead, it was mapping the other way around ```80:8080```.
So I changed this setting and restarted the docker-compose. 

Running ```curl localhost:8080``` again, I got
```
html>
<head><title>502 Bad Gateway</title></head>
<body bgcolor="white">
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.13.5</center>
</body>
</html>
```

After reading various articles, I experimented with changing the proxy_pass of the flaskapp to port 5000  in the flaskapp.conf and also changed the EXPOSE port in Dockerfile to 5000. This enabled the site to load the Welcome webpage.

I attempted to add some items using the forms but got an error:
The redirect was loading an error page at ```localhost,localhost:8000``` 
I honestly didn't understand the reason why I was getting this error. I spent some time on Google looking for a solution but didn't find any. I however asked a collegue about nginx configurations for redirect errors and he pointed me to some [articles](https://www.nginx.com/resources/wiki/start/topics/examples/likeapache/) online where I found that NGINX does not have ProxyPassReverse. The solution was adding a few missing HTTP headers.

Fixing the headers enabled the redirect to load properly but I noticed the page returning ```[,,,]``` with the length increasing with every new entry I made. By using ```curl localhost:8080/success``` and got
```
[<models.Items object at 0x7f10356528d0>, <models.Items object at 0x7f1035652990>, 
<models.Items object at 0x7f1035652a10>, <models.Items object at 0x7f1035652a
90>]
```

Meaning I was returning an object. Also on reviewing the forms.py file, I noticed that the quantity was being passed a StringField instead of an IntegerField and I changed this as well.

To get the result properly printed, I created a result.html where I could take the object being passed and print out the content of the object.

With this, I was able properly display the results in better format. With this is place, I presumed to make the app a basic CRUD by adding Update and Delete functionality to it. This required the addition of an ```edit.html``` file to pass the form contents back to user to edit and save.