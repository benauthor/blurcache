import urllib2
import cookielib

class NewsBlur:
    """NewsBlur API interface"""
    api_url = "http://www.newsblur.com/"

    def __init__(self, username, password):
        """make new NewsBlur instance with username and password"""
        self.username = username
        self.password = password
        self.cj = cookielib.CookieJar()

    def login(self):
        """authenticate with username and password and catch cookie"""
        url = NewsBlur.api_url + "api/login"
        data = "username=" + self.username + "&password=" + self.password
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        self.cj.extract_cookies(response, request)
        return response.read()

    def get_api(self, api_method):
        """generic get request"""
        url = NewsBlur.api_url + api_method
        request = urllib2.Request(url)
        self.cj.add_cookie_header(request)
        response = urllib2.urlopen(request)
        return response.read()

    def logout(self):
        """handy logout shorcut"""
        return self.get_api("api/logout")

    def starred(self):
        """handy get starred items shortcut"""
        return self.get_api("reader/starred_stories")
