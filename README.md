# spidey

This was an exercise for learning more about the Python Scrapy framework.

http://scrapy.org/

The goal was to make a "web spider" that could log into a typical forum and download posts by a particular user.
I just followed the tutorial from the website.  Then I hacked it for a while and figured out my own XPATH
expressions to extract the desired info.

I'm using Python 2.7.10.  I set up a virtual environment with the latest Scrapy version.

The steps for running "spidey" are:

* Activate virtual environment.
* Navigate to top folder of spidey project.
* Enter command:

scrapy crawl spidey -a password=***whatever*** -a nickname=***whomever*** -a post=***number*** -a user=***number*** -a ct=***number*** -o x.json

Another tool can extract data from the json output file.
