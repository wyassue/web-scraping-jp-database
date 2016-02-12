#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import urllib
from bs4 import BeautifulSoup

class DataExtraction(object):

	def execute(self):
		url = "http://www.japannationalfootballteam.com/"
		# info = self.dataListSeason(url)
		# self.detailSeason(url, info)
		# self.dataManager(url)
		self.dataListPlayer(url)

	def getBSObj(self, url):

		try:
			html = urllib.urlopen(url)			
		except HTTPError as e:
			return None

		try:
			bsObj = BeautifulSoup(html.read())	
		except AttributeError as e:
			return None
		return bsObj

	def detailSeason(self, url, data_set=None):
		for season in data_set:
			year = season[0]
			link = url + 'en/' + season[1]
			bsObj = self.getBSObj(link)

			header = [["id","Date","Opponent","Link","H/A","Form","Score","Link Match","Attendance","Venue","Competition"]]
			listSeason = self.getData(bsObj, {"class":"results"},False, year)
			self.write_csv(listSeason,header,"output/detail_season/"+year+".csv")

			header = [['Player','Link','Club','MP','GP','GS','G','PK','YC','RC']]
			listPlayer = self.getData(bsObj, {"class":"stats"})
			self.write_csv(listPlayer,header,"output/player_season/"+year+".csv")

	def dataListPlayer(self,url):
		header = [['Players','Link','Birth Place','Birth Date','GP','G','Debut','Debut – Link','Last Match','Last Match – Link']]
		bsObj = self.getBSObj(url + "en/players/index.html")
		listPlayer = self.getData(bsObj,{"class":"players"}, True)
		self.write_csv(listPlayer,header,"output/players.csv")

	def dataManager(self, url):
		header = [['No.','Manager','GP','Wins','Draws','Losses','GF','GA','GD','First Match','Last','Match','Link']]
		bsObj = self.getBSObj(url + "en/managers.html")
		listManager = self.getData(bsObj,{"class":"managers"})
		self.write_csv(listManager,header,"output/manager.csv")

	def dataListSeason(self,url):
		header = [['Year','Link','GP','Wins','Draws','Losses','GF','GA','GD','Manager(s)']]
		bsObj = self.getBSObj(url + "en/seasons.html")
		listSeason = self.getData(bsObj,{"class":"seasons"})
		self.write_csv(listSeason,header,"output/seasons.csv")

		return listSeason

	def getData(self,data_set, attribute = {}, value_null = False, year = None):

		try:
			listSeason = []
			row = data_set.findAll("table", attribute)

		 	for tr in row:
		 		column = tr.findAll('tr')
		 		for td in column:
					data = []
		 			aaa = td.findAll('td')
		 			for info in aaa:
				 		if(len(info.get_text()) > 0 or value_null):
					 		data.append(info.get_text().encode('utf-8'))
					 		if(len(info.select('a[href]')) != 0):
						 		data.append(info.a['href'])
					if(len(data) > 0):
						listSeason.append(data)
		except Exception:
			return None
		return listSeason

	def write_csv(self, data_set, header=None, filename='test.csv'):		
		b = open(filename, 'w')		
		a = csv.writer(b)
		if(header != None):
			a.writerows(header)
		a.writerows(data_set)
		b.close()
