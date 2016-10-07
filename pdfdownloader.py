'''
Download all pdf files present in the link and save the files
in a given folder
'''
import requests
from bs4 import BeautifulSoup as Bs
from urllib.parse import urlparse,urljoin
import posixpath
import os
import re
from urllib.error import HTTPError
import sys


def download_list(urllist,path):
    for url in urllist:
        filename = posixpath.basename(urlparse(url).path)
        fullname = os.path.join(path,filename)
        download_file(url,fullname)
        

def download_file(url,filename):
    """
    Download the file and save the file to filename
    args:
    url(string)
    filename(string)- path to store the file
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        print("Downloading file-  "+url)
        r = requests.get(url)
    except HTTPError as e:
        print("error downloading file see-"+str(e))
        return
    with open(filename,'wb') as f:
        f.write(r.content)
    

def download_from(url,path):
    """
    The url to download from.
    If the file is a pdf, directly download, else search for .pdfs in the page
    args:
    url(string): url for the page
    path(string): Path to save the download
    """
    u = urlparse(url)
    file_name = posixpath.basename(u.path)
    regex = re.compile(r".*\.pdf")
    pdf_files= []
    if regex.match(file_name):
        pdf_files.append(url)
        
    else:
        try:
            r = requests.get(url).text
        except HTTPError as e:
            print("Error in getting page. "+ str(e))
            return
        soup = Bs(r,"html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href is not None:
                # check if it points to pdf file
                nexturl = urljoin(url,href)
                if regex.match(nexturl):
                    pdf_files.append(nexturl)
                    
    download_list(pdf_files, path) 
    
def main(argv):
    url = argv[1]
    path = argv[2]
    print("Downloading.......")
    print("From.. "+url)
    print("saving in... "+path)
    download_from(url, path)
    print("Finished!")
    
    
if __name__ == "__main__":
    main(sys.argv)
