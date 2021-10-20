"""
	Author: Weng Xiang Heng
	Date: 2021/10/20
"""

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
from tkinter import ttk
import bs4
import requests
import urllib.request as req
import os, sys, time
import threading
import re

# Function
def get_num():
	"""
		從entry拿輸入文字
	"""
		
	num = num_en.get()
	return num

def ask_download():
	file_path = filedialog.askdirectory()
	path_name_en.insert(0, str(file_path))

def get_path():
	file_path = path_name_en.get()
	return file_path

def make_folder(comic_name, file_path):

	comic_name = re.sub('[\/:*?"<>|]', '', comic_name)

	if(os.path.exists(file_path)):
		file_path = file_path + "/漫畫/" + str(comic_name) + "/"

		if(os.path.exists(file_path) == False):
			os.makedirs(file_path)
	else:
		file_path = "./漫畫/" + str(comic_name) + "/"

		if(os.path.exists(file_path) == False):
			os.makedirs(file_path)

	return file_path

def parse_html():
	"""
		請求html
	"""
	global thread_list

	thread_list.append(threading.current_thread())

	word = get_num()
	url = "https://nhentai.net/g/" + word

	url_exist = requests.get(url)

	if(url_exist.status_code != 200):
		message_t.insert('end', "網頁發生錯誤，請重新輸入。\n")
	else:
		request = req.Request(url, headers = {
			"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"}
		)

		with req.urlopen(request) as response:
			data = response.read().decode("utf-8")

		# 解析html, 取得comic name
		root = bs4.BeautifulSoup(data, "html.parser")
		comic_title = root.find("h2", attrs = {"class": "title"})
		comic_name = ''
		for title in comic_title:
			comic_name += title.text

		file_path_main = get_path()
		folder_path = make_folder(comic_name, file_path_main)

		# 第二層
		all_image = root.find_all("a", class_="gallerythumb")
		index = 0
		message_t.insert('end', "------------開始下載-----------\n")
			
		for i in all_image:
			href_level_1 = i.get("href")
			url_level_1 = "https://nhentai.net" + href_level_1
			request = req.Request(url_level_1, headers = {
				"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"}
			)

			with req.urlopen(request) as response:
				data_1 = response.read().decode("utf-8")
			root_1 = bs4.BeautifulSoup(data_1, "html.parser")

			temp_1 = root_1.find("section", attrs = {'id': 'image-container'}, recursive = True)
			temp_2 = temp_1.find("img")
			temp_3 = temp_2.get('src')
		
			html = requests.get(temp_3)
			img_name = folder_path + str(index+1) + '.jpg'

			with open(img_name, 'wb') as file:
				file.write(html.content)
				file.flush()
				file.close()

			show_content = comic_name + str(index+1) + '.jpg' + '......完成(' + str(index+1) + '/' + str(len(all_image)) + ')\n'
			message_t.insert('end',show_content)
			message_t.see("end")

			index = index + 1

		message_t.insert('end', "下載完畢\n")

	if(thread_list != []):
		for num, list_ in enumerate(thread_list):
			if(list_ == threading.current_thread()):
				del thread_list[num]
		# print("DONE")
def fun():
	global thread_list
	
	if(len(thread_list) < 2):
		th = threading.Thread(target = parse_html)		
		th.start()

def clearTextInput():
    message_t.delete("1.0","end")

#============ gui ==================
thread_list = []

win = tk.Tk()

win.title("爬蟲練習v1.0")
win.geometry("320x400+250+250")
win.config()
win.resizable(0, 0)

fontStyle = tkFont.Font(family = "Microsoft JhengHei", size = 11, weight = 'bold')

frame1 = tk.Frame(win, width=100, height=50)

num = tk.Label(frame1, text = "號碼: ", font = fontStyle)
num.pack(padx = (65,0), pady = 5, side = tk.LEFT)

num_en = tk.Entry(frame1, bg = "white", font = fontStyle, width = 12)
num_en.pack(padx = 0, pady = 5, side = tk.LEFT)

frame1.pack(anchor = 'w')

frame2 = tk.Frame(win, width=100, height=50)
path_name = tk.Label(frame2, text = "路徑: ", font = fontStyle)
path_name.pack(padx = (65,0), pady = 5, side = tk.LEFT)

path_name_en = tk.Entry(frame2, bg = "white", font = fontStyle, width = 12)
path_name_en.pack(padx = 0, pady = 5, side = tk.LEFT)

chioce_btn = tk.Button(frame2, text = "選擇", font = fontStyle)
chioce_btn.config(width = 5, height = 1, command = ask_download)
chioce_btn.pack(padx = (10,0), pady = 5, side = tk.LEFT)

frame2.pack(anchor = 'w')

frame3 = tk.Frame(win, width=100, height=50)

ok_btn = tk.Button(frame3, text = "開始", font = fontStyle)
ok_btn.config(width = 10, height = 1, command = fun)
ok_btn.pack(padx = 0, pady = 10, side = tk.LEFT)

frame3.pack()

labelframe = tk.LabelFrame(win, width = 25, labelanchor = tk.N, text = "  LOG  ")
message_t = scrolledtext.ScrolledText(labelframe, height = 10, width = 25, font = fontStyle, wrap=tk.WORD)

message_t.pack()
labelframe.pack()

clean_btn = tk.Button(win, text = "清除", font = fontStyle)
clean_btn.config(width = 10, height = 1, command = clearTextInput)
clean_btn.pack(pady = 10)

win.mainloop()
