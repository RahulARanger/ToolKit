import __pre__
import urllib
import pytube
import re
import os
pytube.__main__.apply_descrambler = __pre__.apply_descrambler
class YTBackend:
	def __init__(self,link):
		self.link=link
		self.obj=pytube.YouTube(self.link)
		self.scrape()
	def scrape(self):
		self.Title=self.obj.title
		
		self.Description=self.obj.description
	def __str__(self):
		print(self.Title)
		return ''
a=YTBackend(input('Enter the Link: '))
print(a)

