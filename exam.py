import pprint
import ipdb

#Multi-word Queries

#Triple Gold Star

#For this question, your goal is to modify the search engine to be able to
#handle multi-word queries.  To do this, we need to make two main changes:

#    1. Modify the index to keep track of not only the URL, but the position
#    within that page where a word appears.

#    2. Make a version of the lookup procedure that takes a list of target
#    words, and only counts a URL as a match if it contains all of the target
#    words, adjacent to each other, in the order they are given in the input.

#For example, if the search input is "Monty Python", it should match a page that
#contains, "Monty Python is funny!", but should not match a page containing
#"Monty likes the Python programming language."  The words must appear in the
#same order, and the next word must start right after the end of the previous
#word.

#Modify the search engine code to support multi-word queries. Your modified code
#should define these two procedures:

#    crawl_web(seed) => index, graph
#        A modified version of crawl_web that produces an index that includes
#        positional information.  It is up to you to figure out how to represent
#        positions in your index and you can do this any way you want.  Whatever
#        index you produce is the one we will pass into your multi_lookup(index,
#        keyword) procedure.

#    multi_lookup(index, list of keywords) => list of URLs
#        A URL should be included in the output list, only if it contains all of
#        the keywords in the input list, next to each other.


def multi_lookup(index, query):
    if len(query) == 0:
        return []
    
    #  get allUrlPos
    allUrlPos = []
    for key in query:
        if not key in index:
            allUrlPos.append([])
        else:
            allUrlPos.append(index[key])
    
    # now iterate through the urls for key0
    results = []
    for url, pos in allUrlPos[0]:
        if isValid(url, pos, allUrlPos):
            results.append(url)
    return results
            

def isValid(url, pos, allUrlPos):
    #===============================
    # base cases
    #===============================
    
    # is the url in first row, with a valid position?
    foundPos = None
    for u, p in allUrlPos[0]:
        if u == url and p == pos:
            foundPos = p
            break
    if not foundPos:
        return False
        
    # are there more rows?
    if len(allUrlPos) == 1:
        return True
    
    #===============================
    # recursive case
    #===============================
    return isValid(url, foundPos+1, allUrlPos[1:])


def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for i in range(len(words)):
        add_to_index(index, words[i], url, i)
        
def add_to_index(index, keyword, url, position):
    if keyword in index:
        index[keyword].append([url, position])
    else:
        index[keyword] = [[url, position]]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None
    



cache = {
   'http://www.udacity.com/cs101x/final/multi.html': """<html>
<body>

<a href="http://www.udacity.com/cs101x/final/a.html">A</a><br>
<a href="http://www.udacity.com/cs101x/final/b.html">B</a><br>

</body>
""", 
   'http://www.udacity.com/cs101x/final/b.html': """<html>
<body>

Monty likes the Python programming language
Thomas Jefferson founded the University of Virginia
When Mandela was in London, he visited Nelson's Column.

</body>
</html>
""", 
   'http://www.udacity.com/cs101x/final/a.html': """<html>
<body>

Monty Python is not about a programming language
Udacity was not founded by Thomas Jefferson
Nelson Mandela said "Education is the most powerful weapon which you can
use to change the world."
</body>
</html>
""", 
}

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None
    







# allUrlPos = [
#                 [['http://www.udacity.com/cs101x/final/b.html', 6], ['http://www.udacity.com/cs101x/final/a.html', 8]],
#                 [['http://mmmmm', 2], ['http://www.udacity.com/cs101x/final/b.html', 7], ['http://www.udacity.com/cs101x/final/a.html', 9]],
#                 [['http://mmmmm', 2], ['http://www.udacity.com/cs101x/final/b.html', 8], ['http://www.udacity.com/cs101x/final/a.html', 10]],
#                 [['http://mmmmm', 2], ['http://www.udacity.com/cs101x/final/b.html', 4], ['http://www.udacity.com/cs101x/final/a.html', 15]]
#             ]
# 
# isValid(url, pos, allUrlPos)
# isValid('http://www.udacity.com/cs101x/final/b.html', 6, allUrlPos) # TRUE

# isValid('http://www.udacity.com/cs101x/final/a.html', 8, allUrlPos) # TRUE



#Here are a few examples from the test site:

# index, graph = crawl_web('http://www.udacity.com/cs101x/final/multi.html')
# multi_lookup(index, ["programming","language"])
# multi_lookup(index, ["arghghg","fuck"])

# print multi_lookup(index, ['Python'])
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

# print multi_lookup(index, ['Monty', 'Python'])
#>>> ['http://www.udacity.com/cs101x/final/a.html']

# print multi_lookup(index, ['Python', 'programming', 'language'])
#>>> ['http://www.udacity.com/cs101x/final/b.html']

# print multi_lookup(index, ['Thomas', 'Jefferson'])
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

# print multi_lookup(index, ['most', 'powerful', 'weapon'])
#>>> ['http://www.udacity.com/cs101x/final/a.html']
