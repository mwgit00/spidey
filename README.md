# spidey

This was an exercise for learning more about the Python Scrapy framework.

http://scrapy.org/

The goal was to make a "web spider" that could log into a typical forum and download posts by a particular user.
I just followed the tutorial from the website.  Then I hacked it for a while and figured out my own XPATH
expressions to extract the desired info.

I used Python 2.7.10.  I set up a virtual environment with the latest Scrapy version.  That was several years ago so who knows what would be required to make any of this work again.

The steps for running "spidey" are:

* Activate virtual environment.
* Navigate to top folder of spidey project.
* Enter command:

scrapy crawl spidey -a password=***whatever*** -a nickname=***whomever*** -a post=***number*** -a user=***number*** -a ct=***number*** -o x.json

Another tool can extract data from the json output file.

-- 

Here are some OpenSSL encryption and decryption commands:

openssl aes-256-cbc -a -salt -in ***plain_text_file*** -out ***ASCII_encrypted_file*** -k *password*

openssl aes-256-cbc -d -a -in ***ASCII_encrypted_file*** -out ***plain_text_file*** -k *password*

Decryption if file was encrypted with older version of OpenSSL:

openssl aes-256-cbc -d -a -md md5 -in ***ASCII_encrypted_file*** -out ***plain_text_file*** -k *password*
