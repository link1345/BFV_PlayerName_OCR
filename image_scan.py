import os

from PIL import Image
import pyocr

import cv2
import numpy as np
import re

from difflib import SequenceMatcher

import asyncio
import settings

class image_scan():
	def __init__(self):
		self.path=settings.Tesseract_path
		self.tessdata_path = settings.Tesseract_tesspath

		os.environ["PATH"] += os.pathsep + self.path
		os.environ["TESSDATA_PREFIX"] = self.tessdata_path

		self.matchNum = 1.0

		self.team1_box_point = [365, 240]
		self.team2_box_point = [1220, 240]
		self.team1_box_end_point = [680, 262]
		self.team2_box_end_point = [1535, 262]
		self.team1_box_size = [self.team1_box_end_point[0]-self.team1_box_point[0], self.team1_box_end_point[1]-self.team1_box_point[1]]
		self.team2_box_size = [self.team2_box_end_point[0]-self.team2_box_point[0], self.team2_box_end_point[1]-self.team2_box_point[1]]

	def ver1_getName(self, fileName, team_box_point, team_box_size, teamName):
		Output_NameList = []
		out_img_num = []

		cv_img = cv2.imread( fileName, 1)

		## -------------------------------
		## -----お好み焼き ----------------
		## -----  精度上げにお使いください--
		## -----  ただし重くなります ------
		k = 1.0
		kernel = np.array([[-k, -k, -k], [-k, 1+8*k, -k], [-k, -k, -k]])
		cv_img = cv2.filter2D(cv_img, ddepth=-1, kernel=kernel)

		#cv_img = cv2.fastNlMeansDenoisingColored(cv_img,None,30, 30, 7, 21)
		## -----------------------------

		# 2極化
		cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
		ret, cv_img = cv2.threshold(cv_img,160,255,cv2.THRESH_BINARY)
		#ret, cv_img = cv2.threshold(cv_img,160,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

		cv_img = cv2.bitwise_not(cv_img)

		cv2.imwrite( "cv_" + fileName , img=cv_img)
		img = Image.open("cv_" + fileName)

		for num in range(1,33):
			start_point=[ team_box_point[0] ,  team_box_point[1] + ( team_box_size[1] * (num - 1)) ]
			end_point=[ start_point[0] + team_box_size[0] ,  start_point[1] + team_box_size[1] ]
			box=(start_point[0],start_point[1],end_point[0],end_point[1])
			#print(num)
			#print(team1_box_size)

			img_crop = img.crop(box)
			img_crop.save( teamName +'\\'+ str(num) +'.png', quality=100)

			cv_img = cv2.imread( teamName +'\\'+ str(num) +'.png', 1)
			cv_img = cv2.resize(cv_img , (int(cv_img.shape[1]*2.5), int(cv_img.shape[0]*2.5)))
			cv2.imwrite( teamName + '\\'+ str(num) +'.png' , img=cv_img)
			user_img = Image.open( teamName + '\\'+ str(num) +'.png')


			#画像から文字を読み込む
			#pyocrへ利用するOCRエンジンをTesseractに指定する。
			tools = pyocr.get_available_tools()

			#print(tool)
			tool = tools[0]
			#print(os.environ.get('PATH'))
			
			builder = pyocr.builders.TextBuilder(tesseract_layout=7)
			text = tool.image_to_string(user_img, builder=builder,lang="eng")
			
			# 色確認
			arr = {}
			
			#arr.append(user_img.shape)
			#arr = set(arr)
			#for c1 in cv_img:
			#	for c2 in c1 :
			#		arr[str(c2)] = ""

			#if len(arr) == 1 :
			#	text = ""

			out_flag = False

			if re.fullmatch(r'[a-zA-Z0-9_-]*', text) == None:
				# これら2つはよく識別間違えを起こすので、補正
				if '/' in text :
					text = text.replace('/', '7')
				if ' ' in text :
					text = text.replace(' ', '')
				
				if re.fullmatch(r'[a-zA-Z0-9_-]*', text) == None:
					out_flag = True

			if out_flag == True:
				#print( str(num) + " : " + text + "  = OUT")
				out_img_num.append(num)
			#else :
				#print( str(num) + " : " + text)

			Output_NameList.append(text)

		#print(Output_NameList)
		return Output_NameList , out_img_num

	# ---------------------------------------


	#OCR対象の画像ファイルを読み込む
	def run(self,fileName):

		print( ' **** image scan ******"' )

		NameList1 , out_img_num1 = self.ver1_getName(fileName, self.team1_box_point, self.team1_box_size, "team1")
		NameList2 , out_img_num2 = self.ver1_getName(fileName, self.team2_box_point, self.team2_box_size, "team2")

		#print(out_img_num1)
		#print(out_img_num2)

		#print(len(out_img_num1))
		#print(len(out_img_num2))


		print(" **********************")


		whitelist = np.loadtxt('whitelist.csv', ndmin=2, delimiter=',', dtype='str',encoding='utf8')
		blacklist = np.loadtxt('blacklist.csv', ndmin=2, delimiter=',', dtype='str',encoding='utf8')
		blacklist_clan = np.loadtxt('blacklist_clan.csv', ndmin=2, delimiter=',', dtype='str',encoding='utf8')

		#print(len(whitelist))

		#exit()

		def user_search(playerlist,whitelist, blacklist, blacklist_clan):
			black_hit_user = []
			
			#print(blacklist)

			for user in playerlist :
				out_hit = False
				safe_hit = False

				def blacklist_put(b_clan,user):
					out_hit = False
					user_clan = re.search(r'([\|\]\}\[\{0-9a-zA-Z]{1,6}]|[\|\]\}\[\{0-9a-zA-Z]{1,6}}|[\|\]\}\[\{0-9a-zA-Z]{1,6}\|)', user)
					
					if user_clan != None :
						c_user = user_clan.group()
						c_user = c_user.replace('[', '')
						c_user = c_user.replace(']', '')
						c_user = c_user.replace('{', '')
						c_user = c_user.replace('}', '')
						c_user = c_user.replace('|', '')
						r = SequenceMatcher(None, b_clan, c_user).ratio()
						if  r >= self.matchNum :
							out_hit = True
							print("clan hit")
						return out_hit

				for b_clan in blacklist_clan :
					out_hit = blacklist_put(b_clan[0], user)

				for b_user in blacklist :
					#print( b_user + "  " + user )
					r =  SequenceMatcher(None, b_user[0], user).ratio()
					#print(r)
					if r >= self.matchNum :
						out_hit = True
						break
				
				for w_user in whitelist :
					r =  SequenceMatcher(None, w_user[0], user).ratio()
					if r >= self.matchNum :
						safe_hit = True
						break
				
				if out_hit == True and safe_hit == False :
					print('Black User:  ' + user )
					black_hit_user.append( user )
			
			return black_hit_user


		print(" **** Team1 Search ****")
		b_team1 = user_search(NameList1, whitelist, blacklist, blacklist_clan)

		print(" **********************")
		print(" **** Team2 Search ****")
		b_team2 = user_search(NameList2, whitelist, blacklist, blacklist_clan)

		print(" **********************")


		return NameList1, NameList2, b_team1, b_team2