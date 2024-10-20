import re
from urllib.parse import urlparse, urljoin
from lxml import html

def scraper(url, resp):
    links = extract_next_links(url, resp)

    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp is of type Response
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if resp.status != 200:
        print(f'ERROR : {resp.error}')
        # error with this link: https://ics.uci.edu/events/category/department-seminars/
        return []
    
    link_list = []
    
    lxmlContent = html.fromstring(resp.raw_response.content) # faster than BeautifulSoup so opted for this
    anchor_tags = lxmlContent.xpath('//a/@href') # gets all anchor tags in HTML
    for retrieved_link in anchor_tags:
        a_URL = check_if_complete_URL(retrieved_link, resp.raw_response.url)
        if (valid_content): # to prevent getting stuck in calendar
            link_list.append(a_URL)
  
    return link_list

def valid_content(resp): # will have to add more checks to prevent traps
    return "No event" not in resp.raw_response and "No results" not in resp.raw_response

def check_if_complete_URL(link, current_url):
    '''
        Checks if the link is a complete or relative URL. If complete it returns a string URL. If not complete, it
        combines the current pages URL with the relative one.
    '''
    if urlparse(link).scheme == '':
        return urljoin(current_url, link)
    else:
        return link
        
    


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    '''THERE MAY BE MORE TO CONSIDER '''
    try:
        potential_domains = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu","stat.uci.edu", "today.uci.edu"]
        parsed = urlparse(url)
        
        '''
        Checks if it is within the given domains
        '''
        if isinstance(parsed.netloc, bytes):
            netloc = parsed.netloc.decode('utf-8')
            path = parsed.path.decode('utf-8')
        else:
            netloc = parsed.netloc
            path = parsed.path
        print(f"NETLOC PATH: {netloc}, {path}")

        flag = False
        if netloc in potential_domains:
            if netloc == "today.uci.edu" and "department/information_computer_sciences" not in path:
                return False
        else:
            return False

        print(f"MADE IT {parsed}")
        if parsed.scheme not in set(["http", "https"]):
            return False
            
    
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
