from bs4 import BeautifulSoup
import requests
import json 

#url = "https://cyberleninka.ru/article/n/otsenka-effektivnosti-parallelnyh-algoritmov-dlya-modelirovaniya-mnogosloynogo-perseptrona"

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

	#soup = BeautifulSoup(get_from_cache(url), 'html.parser')
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	
	data.update({ 'url' : url })

	name = soup.find('i', itemprop = 'headline').get_text()
	data.update({ 'name' : name })

	for a in soup.findAll('li', itemprop = 'author'):
		authors.update( { id : (a.span.get_text()) } )
		id += 1
	if authors:
		data.update({'authors' : authors})
	else: 
		pass

	try:
		for k in soup.find('i', itemprop = 'keywords').findAll('span'):
			keywords.append(k.get_text())
		data.update({ 'keywords' : [ _.lower() for _ in keywords ]}) 
	except AttributeError: 
		pass
		#data.update({ 'keywords' : [] })

	try: 
		anno = soup.find('p', itemprop = 'description').get_text()
		data.update({ 'annotation' : anno })
	except AttributeError: 
		pass
		#data.update({ 'annotation' : "" })
	
	#return data
	return json.dumps(data, ensure_ascii=0, indent = 4)

if __name__ == '__main__':
#	print(get_article_info(url))
	f = open('urls.txt')
	for line in f.readlines():
		print(get_article_info(line.rstrip()))
