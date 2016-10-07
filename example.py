import requests
from bs4 import BeautifulSoup as Bs
import re
'''
html = requests.get("http://www.pythonscraping.com/pages/warandpeace.html").text
bsobj = Bs(html,"html.parser")

for name in bsobj.find_all("span",{'class':"green"}):
    print(name.get_text())
'''  
# A bit of re

html = requests.get("http://www.pythonscraping.com/pages/page3.html").text
bsobj = Bs(html,"html.parser")
images = bsobj.findAll("img",{'src':re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
for image in images:
    print(type(image))