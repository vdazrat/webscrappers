import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import queue

'''
Simple graph object
implement it with dicts itself, with label being number.
Keep a dict that maps url to the id
'''

class URLMap:
    """
    Map of internal urls with ids.
    Also maintains a list of external URLs.

	Args:
        urlList(:obj:'list',optional): list of url strings
    Attributes:
        url_to_id(dict) - a dict mapping url to an id
	    id_to_url(dict) - a reverse dict of url_to_id
		count(int) - number of urls
	"""
		
    def __init__(self,urlList=None):
		# should have another list for external map as well
        if urlList  is None:
            urlList = []
        # Convert a list to dict
        self.url_to_id = {val:i for i,val in enumerate(urlList)}
        self.id_to_url = {i:val for i,val in enumerate(urlList)}
        # Maintain a counter for the list or urls so far
        self.count = len(urlList)
		
    def add(self,url):
        """
	    Add a url to the map.
	    Args:
		url(str): a url string
		"""
        if url not in self.url_to_id:
            self.url_to_id[url] = self.count
            self.id_to_url[self.count] = url
            self.count += 1

class URLGraph:
    """
	This is a class for a directed url graph.
	Args:
	connectedList(:obj:'list',optional): list of tuples of url strings
	
	Attributes:
	urlmap(:obj:'URLMap'): URLMap object
	_graph(dict): A dict mapping implementation of a graph
	"""
    def __init__(self,connectedList = None):
        self._graph = {}
        if connectedList is None:
	        connectedList = []
		# Build the graph from the connectedList
        # first, create a urlmap of the list
        self.urlmap = URLMap()
        # cleanup this code, looks mucky. 
        for (u1,u2) in connectedList: # add each url to the urlmap
            self.urlmap.add(u1)	
            self.urlmap.add(u2)	

        for (u1,u2) in connectedList:
            # add it to _graph
            urlid1,urlid2 = self.urlmap.url_to_id[u1],self.urlmap.url_to_id[u2]			
            if self._graph.get(urlid1,0) == 0:
                self._graph[urlid1] = []
            if urlid2 not in self._graph[urlid1]:
                self._graph[urlid1].append(urlid2)			

		

def makeURLGraph(url):
    """
    Factory method to create a URLGraph from a url
    Traverses each link in BFS order.
    Algorithm:
    1. mark x as visited
    2. get all hrefs l[] from a url x
    3. add (x,y) in connetedlist for each l 
    4. x = y for each l
	Args:
    url: string, a web url
	"""
    # use requests to get the web page request
    urlmap = URLMap()
    p_firsturl = urlparse(url)
    urlmap.add(url)
    connectedList = []
    visitedList = []
    nodeQueue = queue.Queue() # is the next node to explore
    nodeQueue.put(urlmap.url_to_id[url])
    while not nodeQueue.empty():
        nexturl = urlmap.id_to_url[nodeQueue.get()]
        data = requests.get(nexturl).text
        soup = BeautifulSoup(data,"html.parser")
        visitedList.append(urlmap.url_to_id[nexturl]) # to check cycles
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                parsed_url = urlparse(href)
                if parsed_url.netloc == p_firsturl.netloc:
                    connectedList.append((nexturl,parsed_url.geturl()))
                    urlmap.add(href)
                    if urlmap.url_to_id[href] not in visitedList:
                        nodeQueue.put(urlmap.url_to_id[href])

    return URLGraph(connectedList)

    
            

def __main__(): 
    ulist = ['www.g.com/1','www.g.com/2']
    map  = URLMap(ulist)
    map.add('www.g.com/3')
    #print(map.urlmap)
    connectedList = [('www.g.com/1','www.g.com/2'),('www.g.com/2','www.g.com/3'),('www.g.com/3','www.g.com/2'),('www.g.com/3','www.g.com/1')]
    ug = URLGraph(connectedList)
    print(ug._graph)
	
if __name__ == '__main__':
    ug = makeURLGraph('http://www.vdasarat.xyz/')
    print(ug._graph)