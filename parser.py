from bs4 import BeautifulSoup
import requests
import json 

url = "https://cyberleninka.ru/article/n/gipertrofiya-levogo-zheludochka-serdtsa-diagnostika-posledstviya-i-prognoz"

# def get_from_cache(url = ""):
# 	fname = url.split('/')[-1]
# 	try:
# 		rez = open("database/%s.dat" % fname, 'rb').read().decode('UTF-8')
# 	except FileNotFoundError:
# 		rez = requests.get(url).text
# 		open("database/%s.dat" % fname, 'w').write(rez)
# 	return rez

def get_article_info(url = ""): # rez
	data = {}
	authors = {}
	keywords = []
	id = 1

	data['url'] = url

	#soup = BeautifulSoup(get_from_cache(url), 'html.parser')
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')

	name = soup.find('i', itemprop = 'headline').get_text()
	data['name'] = name

	for a in soup.findAll('li', itemprop = 'author'):
		authors.update( { id : (a.span.get_text()) } )
		id += 1
	data.update({'authors' : authors})

	for k in soup.find('i', itemprop = 'keywords').findAll('span'):
		keywords.append(k.get_text())
	data['keywords'] = [ _.lower() for _ in keywords ]

	anno = soup.find('p', itemprop = 'description').get_text()
	data['annotation'] = anno
	
	return data
	#return json.dumps(data, ensure_ascii=0, indent = 4)

if __name__ == '__main__':
	print(get_article_info(url))
