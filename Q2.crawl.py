# Yael Magid 209134956
import requests
import lxml.html
import time


# class for save the importent things
class UrlNode:
    def __init__(self, url, father_url):
        self.url = url
        self.father = father_url
        self.rank = 0
        self.is_crawled = False


# add the node to the urls list
def add_to_urls_list(node, urls_list):
    # if url_node is seen already, then rise the rank, else - add to list
    for url_node in urls_list:
        if node.url == url_node.url:
            node.rank += 1
            if url_node.father.url == node.father.url:
                url_node.rank += 1
                return
            if url_node.rank < node.rank:  # update current node to higher place
                url_node.rank = node.rank
                url_node.father = node.father
                return
    urls_list.append(node)


# choose the next node from the urls_list
def get_next_node(urls_list, node):
    curr_node = None
    # if node is visited - ignor.
    for n in urls_list:
        if not n.is_crawled:
            curr_node = n
            break
    # if all the nodes are visited
    if curr_node == None:
        return False, None
    # check for higher priority
    for n in urls_list:
        if curr_node.rank < n.rank and not n.is_crawled:
            curr_node = n
    if curr_node != None:
        return True, curr_node
    return False, None


# add the prefix
def add_url_prefix(url):
    return "https://en.wikipedia.org" + url


def crawl_url(url_node, urls_list, xpaths, count):
    # if we did 100 recursive calls, stop
    if count > 100:
        return urls_list
    # extract the html
    res = requests.get(url_node.url)
    doc = lxml.html.fromstring(res.content)
    # mark node as visited
    url_node.is_crawled = True

    # if there is some xpaths
    for xpath in xpaths:
        # for every url that stand under the conditions
        for child_url in doc.xpath(xpath):
            child_url = add_url_prefix(child_url)
            child_node = UrlNode(child_url, url_node)
            # url seen - so rank increased
            child_node.rank += 1
            # add to the list
            add_to_urls_list(child_node, urls_list)
    #rise the count
    count += 1
    # continue the next url
    can_crawl = True
    while can_crawl:
        can_crawl, next_node = get_next_node(urls_list, url_node)
        if not can_crawl:
            break
        try:
            time.sleep(1)
            return crawl_url(next_node, urls_list,xpaths, count)
        except:
            next_node.is_crawled = True
    return urls_list

# first crawl function
def crawl(url, xpaths):
    # seen urls
    urls_list = []
    # counting to 100
    count = 0
    # create the first node
    url_node = UrlNode(url, None)
    # after seeing the url - rise the rank
    url_node.rank += 1
    urls_list.append(url_node)
    # recursive helper function
    urls_list = crawl_url(url_node, urls_list, xpaths, count)
    # create the solution list and return it
    solution = []
    for node in urls_list:
        if node.father is None:
            continue
        solution.append([node.father.url, node.url])
    return solution