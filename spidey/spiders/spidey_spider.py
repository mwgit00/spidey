import scrapy
import url_info as uix
from spidey.items import SpideyItem


class SpideySpider(scrapy.Spider):
    name = "spidey"
    allowed_domains = [uix.DOMAIN]
    start_urls = [
        uix.START
    ]

    def __init__(self, ct=None, user=None, post=None, nickname=None, password=None, *args, **kwargs):
        super(SpideySpider, self).__init__(*args, **kwargs)
        self.ct = 1  # number of pages to crawl
        self.user = ""  # user ID (can be anybody)
        self.post = ""  # first post ID
        self.password = ""  # user password (can be anything)
        self.nickname = ""  # user nickname (can be anybody)
        if nickname is not None:
            self.nickname = str(nickname)
        if password is not None:
            self.password = str(password)
        if post is not None:
            self.post = str(post)
        if user is not None:
            self.user = str(user)
        if ct is not None:
            self.ct = int(ct)
        self.first_post_url = uix.USERS + "/" + self.user + "/posts/" + self.post

    def parse(self, response):
        # must begin by logging in
        return scrapy.FormRequest.from_response(response,
                formdata={'user[login]': self.nickname, 'user[password]': self.password},
                callback=self.after_login)

    def after_login(self, response):
        # check for magic string to determine log-in success
        print 'AFTER LOGIN ATTEMPT...'
        print response
        if "not able to find you" in response.body:
            print "*** D'OH!!! ***"
            return
        else:
            print "STARTING AT " + self.post
            yield scrapy.Request(url=self.first_post_url, callback=self.parse_tastypage)

    def parse_tastypage(self, response):
        # title and date have simple xpath
        s_title = response.xpath(uix.XPATH_TITLE).extract()[0]
        s_datetime = response.xpath(uix.XPATH_DATETIME).extract()[0]
        print "title: ", s_title
        print "date:  ", s_datetime

        # link to next post has a long xpath
        # but must also handle case if next post does not exist
        q0 = response.xpath(uix.XPATH_POST1)
        q1 = q0.xpath(uix.XPATH_POST2)
        print q0
        print q1
        s_next_url = ""
        url_extractor = q1.extract()
        if url_extractor:
            s_next_url = q1.extract()[0]
        
        # category must be found based on class name
        # then remove whitespace
        xp_category = response.xpath(uix.XPATH_CATEGORY).extract()
        s_category = xp_category[0].strip()

        # writing text must be found based on class name
        # it may have multiple 'p' sections
        xp_writing = response.xpath(uix.XPATH_WRITING)

        print "dood ", s_title, s_datetime, response.url, self.ct
        s_writing = ""
        for each in xp_writing:
            print ":::  ", each.extract()
            s_writing += each.extract()
        print s_writing

        item = SpideyItem()
        item['title'] = s_title
        item['date'] = s_datetime
        item['link'] = response.url
        item['category'] = s_category
        item['writing'] = s_writing
        yield item

        # stop if next URL is blank
        if not s_next_url:
            return

        # stop if desired number of pages have been crawled
        self.ct -= 1
        if self.ct is 0:
            return

        # create link for next post and scrape it
        new_url = uix.NEXT + s_next_url
        yield scrapy.Request(url=new_url,
                            callback = self.parse_tastypage)

