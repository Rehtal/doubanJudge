# -*- coding:utf-8 -*-

# Name: extractHistoryInfo_HTML.py
# Author: Rehtal
# Date: 2011.11.8
# Description:
# Implementation of class of extracting useful
# information from normal html pages.

# PATCH:
# 	1, douban will forbid too many requests in a certain time.
# Can use api or use sleep() function to slow down the access time.

import re
import urllib2
from BeautifulSoup import BeautifulSoup

class extractHistoryInfo_HTML:
	def __init__(self, userId):
		"""para:
			in -userId-: douban user id."""
		
		# Collect info by userId.
		self.userId = userId;
		
		# Collected info.
		# 1, Book part
		self.bookInfo = {'collect':[], 'wish':[], 'do':[]};
		self.bookScore= {'collect':0, 'wish':0, 'do':0};
		self.bookTypeList = ['collect', 'wish', 'do']

		# PATCH:Can extend more kind of info such as "groupInfo", "replyInfo" etc.
	
	def feed(self):
		"""Begin collecting info we need"""
		# Book part.
		self.getBookInfo()
		self.computeBookScore()

		# PATCH:Other extended part.
	
	def smartPrint(self):
		"""Output collected info in 'smart' way.
		PATCH:Real smart output."""

		# Book part.
		print 'SCORE:'
		for bootType in self.bookTypeList:
			print bookType+':'+str(self.bookScore)

		# PATCH:Can extend more kind of info.
		
	def getBookInfo(self):
		"""Collect user's book records incluing 3 parts that saved in self.bookTypeList:
		1, Already read, marked as 'collect'
		2, Want to read, marked as 'wish'
		3, Reading now, marked as 'do'"""

		for bookType in self.bookTypeList:
			print 'Begin type:'+bookType
			# Construct site address.
			site = 'http://book.douban.com/people/'+self.userId+'/'+bookType
			# Request html page from douban.
			page = urllib2.urlopen(site)
			
			# Deliver the whole page to self.extractBookInfo function.
			# If there are more than one page need to be handled,
			# the self.extractBookInfo function will auto do it.
			self.extractBookInfo(page, bookType)

	def computeBookScore(self, bookType=True):
		"""After getting history records we need, it'll be quite easy to
		compute the estimate score.
		
		In this version(0.1), we haven't yet complete the background databases
		for scoring each record.

		So we change a way by using the douban score instead.
		
		para:
			in -bookType-:Book type that need to handle, default as all types."""	
		for bookType in self.bookTypeList:
			print 'Scoring:'+bookType
			for singleRecord in self.bookInfo[bookType]:
				print '\t'+singleRecord
				# Get each page and feed it to BeautifulSoup
				page = urllib2.urlopen(singleRecord)
				soup = BeautifulSoup(page)

				# PATCH:Below
				# In each page we only need two small pieces:
				# 1, The average point.
				# 2, How many people assessed this book.
				# Thus we are facing a incredible big problem:
				# WE NEED TO LOAD THE WHOLE PAGE JUST FOR TWO SMALL PARTS OF IT.
				# This action will make the program runs very slow.
				# In later version we can use douban APIs instead of loading the
				# whole page.
				scoreTag = soup.find('strong', attrs={'property':'v:average'})
				assessNumTag = soup.find('span', attrs={'property':'v:votes'})

				# PATCH:Below
				# Here is the most important part of this function:
				# HOW TO GIVE A RELIABLE ESTIMATE SCORE.  
				# In this version(0.1), we simply use plus operation.  
				# However, it's obvious such method can not give out a good result.  
				#
				# For instance: 
				# 	1, A book is only assessed by a few people and scored 9.
				# 	2, While another book is assessed by about 1000 people, and scored 9
				# In this case, the score of the second book is definitely more
				# reliable than the first one. 
				# 
				# The plus operation cannot differentiate the two conditions.
				# In later version, the operation of score should be changed 
				# to a distribution of probability.
				if scoreTag.string!=None:
					self.bookScore[bookType] += float(scoreTag.string)

	# All functions below is used inside the class.
	# WARNING: Call below functions may cause unknown results.
	def extractBookInfo(self, page, bookType):
		"""Extract records from given html page.
		Store extracted data to self.bookInfo.
		There are exactly 2 steps in this fucntion.
		1, Extract records and save to self.bookInfo.
		2, If there are more than one page need to be handled,
		the function will recursively call itself.
		
		para: 
			in -page-: urllib2.urlopen return type, the loaded page.
			in -bookType-: the type of book, may be 'collect', 'wish', 'do'"""
		# STEP 1: Extract.
		# Use soup to get records  
		soup = BeautifulSoup(page)
		print '\tworking...'

		# Book href regular expression.
		bookRe = re.compile('http://book.douban.com/subject/[0-9]+/')
		# Title exist regular expression.
		titleExist = re.compile('.+')

		# EXPLANATION OF TITLEEXIST
		# 	Each web page of douban book contain two 'anchor tag' point to a same book.
		# We need one and only one. So the other must be eliminated.
		# 	After checking the pattern of the two 'anchor tag', we can find out that 
		# these two tags look a little different.
		# 1, One kind of look.
		# 	<a title='Made to Stick' href='http://book.douban.com/subject/1963552/', class='nbg'>
		# 2, The other kind of look.
		# 	<a href="http://book.douban.com/subject/1963552/">
		# CONCLUSION:
		# 	By checking whether the 'title attribute' exists we can pick out 
		# only one from the two.

		# Get them and save them!
		bookRecords = soup.findAll('a', attrs={'href':bookRe, 'title':titleExist})
		self.bookInfo[bookType].extend([a['href'] for a in bookRecords])

		# STEP 2: Recursive.
		morePage = soup.find('div', attrs={'class':'paginator'})
		# Make sure there indeed are more pages.
		# Then find the next page href.
		while morePage and getattr(morePage, 'string', None) != u'后页&gt;':
			morePage = morePage.next
		# Reaffirm that there indeed are more pages.
		if morePage:
			page = urllib2.urlopen(morePage['href'])
			self.extractBookInfo(page, bookType)

# Below is testing codes.
if __name__ == '__main__':
	e = extractHistoryInfo('pongba')
	e.getBookInfo()
	print 'loading finish.'
	e.computeBookScore('collect')
	print 'compute score finish.'
	print 'score:'+str(e.bookScore['collect'])
