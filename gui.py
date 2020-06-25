import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as scrolledtext
import bs4
import requests
import urllib.request as req
import os, sys, time
import threading
#304187
#315993
#316018

#function
#從entry拿輸入文字
def get_word():
	num = num_en.get()
	return num

def parse_html():
#請求html
	word = get_word()
	url = "https://nhentai.net/g/" + word
	request = req.Request(url, headers = {
		"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"}
	)

	with req.urlopen(request) as response:
		data = response.read().decode("utf-8")
	#message_t.insert('end', "連線成功，下載中........\n")
#解析html
	#取得comic name
	root = bs4.BeautifulSoup(data, "html.parser")
	comic_name_ = root.find("h2", attrs = {"class": "title"})
	comic_name = ''
	for j in comic_name_:
		comic_name += j.text
#	while(True):
#		pass
#儲存位置,主資料夾
	folder_path = ".\\漫畫\\" + str(comic_name) + "\\"

	if(os.path.exists(folder_path) == False):
	   os.makedirs(folder_path)

#第二層
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

		show_content = comic_name + str(index+1) + '.jpg' + '......完成\n'
		message_t.insert('end',show_content)
		message_t.see("end")

		index = index + 1

		time.sleep(1)
	message_t.insert('end', "下載完畢\n")
	print("DONE")

def fun():
	th = threading.Thread(target = parse_html)
	th.start()

def clearTextInput():
    message_t.delete("1.0","end")

#============ gui ==================
win = tk.Tk()

win.title("爬蟲練習v1.0")
win.geometry("330x320+250+250")
win.config()
win.resizable(0, 0)

fontStyle = tkFont.Font(family = "Microsoft JhengHei", size = 11, weight = 'bold')
fontStyle1 = tkFont.Font(family = "Microsoft JhengHei", size = 11, weight = 'bold')

frame1 = tk.Frame(win, width=100, height=50)

num = tk.Label(frame1, text = "神的語言: ", font = fontStyle)
num.pack(padx = 0, pady = 5, side = tk.LEFT)

num_en = tk.Entry(frame1, bg = "white", font = fontStyle1, width = 12)
num_en.pack(padx = 5, pady = 5, side = tk.LEFT)

frame1.pack()

frame2 = tk.Frame(win, width=100, height=50)

ok_btn = tk.Button(frame2, text = "開始", font = fontStyle)
ok_btn.config(width = 10, height = 1, command = fun)
ok_btn.pack(padx = 0, pady = 10, side = tk.LEFT)


clean_btn = tk.Button(frame2, text = "清除", font = fontStyle)
clean_btn.config(width = 10, height = 1, command = clearTextInput)
clean_btn.pack(padx = 20, pady = 10, side = tk.LEFT)

frame2.pack()

labelframe = tk.LabelFrame(win, width = 25, labelanchor = tk.N, text = "  LOG  ")
message_t = scrolledtext.ScrolledText(labelframe, height = 10, width = 25, font = fontStyle, wrap=tk.WORD)

message_t.pack()
labelframe.pack()

win.mainloop()