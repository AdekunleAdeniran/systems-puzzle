# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Introduction](README.md#introduction)
3. [Puzzle details](README.md#puzzle-details)
4. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
5. [FAQ](README.md#faq)

# Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

# Introduction

Imagine you're on an engineering team that is building an eCommerce site where users can buy and sell items (similar to Etsy or eBay). One of the developers on your team has put together a very simple prototype for a system that writes and reads to a database. The developer is using Postgres for the backend database, the Python Flask framework as an application server, and nginx as a web server. All of this is developed with the Docker Engine, and put together with Docker Compose.

Unfortunately, the developer is new to many of these tools, and is having a number of issues. The developer needs your help debugging the system and getting it to work properly.

# Puzzle details

The codebase included in this repo is nearly functional, but has a few bugs that are preventing it from working properly. The goal of this puzzle is to find these bugs and fix them. To do this, you'll have to familiarize yourself with the various technologies (Docker, nginx, Flask, and Postgres). You definitely don't have to be an expert on these, but you should know them well enough to understand what the problem is.

Assuming you have the Docker Engine and Docker Compose already installed, the developer said that the steps for running the system is to open a terminal, `cd` into this repo, and then enter these two commands:

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. After that you can run the whole system with:

    docker-compose up -d

At that point, the web application should be visible by going to `localhost:8080` in a web browser. 

Once you've corrected the bugs and have the basic features working, commit the functional codebase to a new repo following the instructions below. As you debug the system, you should keep track of your thought process and what steps you took to solve the puzzle.

## Instructions to submit your solution
* Don't schedule your interview until you've worked on the puzzle 
* To submit your entry please use the link you received in your systems puzzle invitation
* You will only be able to submit through the link one time
* For security, we will not open solutions submitted via files
* Use the submission box to enter the link to your GitHub repo or Bitbucket ONLY
* Link to the specific repo for this project, not your general profile
* Put any comments in the README inside your project repo

# FAQ

Here are some common questions we've received. If you have additional questions, please email us at `devops@insightdata.com` and we'll answer your questions as quickly as we can (during PST business hours), and update this FAQ. Again, only contact us after you have read through the Readme and FAQ one more time and cannot find the answer to your question.

### Which Github link should I submit?
You should submit the URL for the top-level root of your repository. For example, this repo would be submitted by copying the URL `https://github.com/InsightDataScience/systems-puzzle` into the appropriate field on the application. **Do NOT try to submit your coding puzzle using a pull request**, which would make your source code publicly available.

### Do I need a private Github repo?
No, you may use a public repo, there is no need to purchase a private repo. You may also submit a link to a Bitbucket repo if you prefer.

### What sort of system should I use to run my program (Windows, Linux, Mac)?
You should use Docker to run and test your solution, which should work on any operating system. If you're unfamiliar with Docker, we recommend attending one of our Online Tech Talks on Docker, which you should've received information about in your invitation. Alternatively, there are ample free resources available on docker.com.

### How will my solution be evaluated?
While we will review your submission briefly before your interview, the main point of this puzzle is to serve as content for discussion during the interview. In the interview, we'll evaluate your problem solving and debugging skills based off how you solved this puzzle, so be sure to document your thought process.

### This eCommerce site is ugly...should I improve the design?  
No, you should focus on the functionality. Your engineering team will bring on a designer and front-end developer later in the process, so don't worry about that aspect in this puzzle. If you have extra time, it would be far better to focus on aspects that make the code cleaner and easier to use, like tests and refactoring.

### Should I use orchestration tools like Kubernetes?
While technologies like Kubernetes are quite powerful, they're likely overkill for the simple application in this puzzle. We recommend that you stick to Docker Compose for this puzzle.

### Solution Approach
After running the codes
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

After reading up of various articles, I experimented with changing the proxy_pass of the flaskapp to port 5000  in the flaskapp.conf and also changed the EXPOSE port in Dockerfile to 5000. This enabled the site to load the Welcome webpage.

I attempted to add some items using the forms but got an error:
The redirect was loading an error page at ```localhost,localhost:8000``` 
I honestly didn't understand the reason why I was getting this error. I spent some time on Google looking for a solution but didn't find any. I however asked a collegue about nginx configurations for redirect errors and he pointed me to some [articles](https://www.nginx.com/resources/wiki/start/topics/examples/likeapache/) online where I found that NGINX does not have ProxyPassReverse. The solution was adding a few missing HTTP headers.

Fixing the headers enabled the redirect to load properly but I noticed the page returning ```[,,,]``` with the length increasing with every new entry I made. By using ```curl localhost:8080/success``` and got
```
[<models.Items object at 0x7f10356528d0>, <models.Items object at 0x7f1035652990>, <models.Items object at 0x7f1035652a10>, <models.Items object at 0x7f1035652a
90>]
```

Meaning I was returning an object. Also on reviewing the forms.py file, I noticed that the quantity was being passed a StringField instead of an IntegerField and I changed this as well.

To get the result properly printed, I created a result.html where I could take the object being passed and print out the content of the object.

With this, I was able properly display the results in better format. With this is place, I presumed to make the app a basic CRUD by adding Update and Delete functionality to it.