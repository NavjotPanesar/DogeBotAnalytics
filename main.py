#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
import webapp2
from google.appengine.ext import db
import datetime

class MainHandler(webapp2.RequestHandler):
    def post(self):
        self.handleTweetInfo()

    def handleTweetInfo(self):
        token = self.request.get("token")
        if token != "wow":
            self.response.write("Authentication Failed")
            return
        tweet = Tweet()
        tweet.tweetId = int(self.request.get("tweetId", 0))
        tweet.username = self.request.get("username", None)
        tweet.command = self.request.get("command", None)
        tweet.commandOperands = self.request.get("commandOperands", "")
        tweet.timeTaken = int(self.request.get("time", 0))
        if tweet.tweetId is not 0 and tweet.username and tweet.command and tweet.timeTaken is not 0:
            if self.checkIfTweetExists(tweet.tweetId) is False:
                tweet.put()
                self.response.write("0")
            else:
                self.response.write("Duplicate Data")
        else:
            self.response.write("Invalid Parameters")

    def checkIfTweetExists(self, tweetId):
        #there has got to be a better way to do this
        q = Tweet.all()
        q.filter("tweetId =", tweetId)
        for p in q.run(limit=1):
            return True
        return False


class Tweet(db.Model):
    """Models a single tweet command"""
    tweetId = db.IntegerProperty()
    username = db.StringProperty()
    command = db.StringProperty()
    commandOperands = db.StringProperty()
    timeTaken = db.IntegerProperty(indexed=False)
    date = db.DateTimeProperty(auto_now_add=True)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
