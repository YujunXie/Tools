import os
import requests
import urllib.request
import json
from bs4 import BeautifulSoup

url = "http://stars.haibao.com/star/list/"
root = 'mx/'

#first index
sex = ['1', '2']
#second index
area = ['2', '3', '4', '5']
#third index
sortby = '1'
#page index
pages = ['/', '/2.html', '/3.html', '/4.html']

def get_content(path):

	res = requests.get(path)

	if res.status_code == 404:
		print(" 404 error")
		return False

	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text, "lxml")

	return soup

for seg1 in sex:

	for seg2 in area:

		for page in pages:

			if seg2 == '2' and page == '2.html':
				break
			if seg2 == '3' and page == '2.html':
				break
			if seg2 == '4' and page == '4.html':
				break

			path = url + seg1 + '-' + seg2 + '-0-0-' + sortby + page

			print(path)

			soup = get_content(path)

			if soup == False:
				continue
			
			lists = soup.find("ul", class_="u-star").find_all("li")

			for star in lists:

				star_temp = star.find("div", class_="img").find("a")
				img_url = star_temp.find("img")['src']
				name = star_temp['title'].replace('/', '')

				print(img_url)
				print(name)
				
				img_dir = root + name + '/'
				if not os.path.exists(img_dir):
					os.mkdir(img_dir)

				headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

				t_request = urllib.request.Request(url=img_url, headers=headers)
				img = urllib.request.urlopen(t_request).read()
				with open(img_dir + name + ".jpg", 'wb') as f:
					f.write(img)

				
				#urllib.request.urlretrieve(img_url, img_dir + "%s.jpg" % name, Schedule)
