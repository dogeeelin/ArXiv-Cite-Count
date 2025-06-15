import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
from fake_useragent import UserAgent

def get_google_scholar_citation(arxiv_url):
    """
    Get citation count from Google Scholar for a given ArXiv paper
    
    Args:
        arxiv_url (str): URL of the ArXiv paper
        
    Returns:
        int: Citation count from Google Scholar, or None if not found
    """
    try:
        # Extract ArXiv ID from URL
        parsed = urlparse(arxiv_url)
        if 'arxiv.org' not in parsed.netloc:
            raise ValueError("Not an ArXiv URL")
            
        # Handle different ArXiv URL formats
        path_parts = parsed.path.strip('/').split('/')
        if path_parts[0] == 'abs':
            arxiv_id = path_parts[1]
        elif path_parts[0].isdigit():  # Old format
            arxiv_id = '/'.join(path_parts[:2])
        else:
            raise ValueError("Could not extract ArXiv ID from URL")
        
        # Create Google Scholar search URL
        gscholar_url = f"https://scholar.google.com/scholar_lookup?arxiv_id={arxiv_id}"
        print(f"Google Scholar URL: {gscholar_url}")
        
        # Set up headers with a random user agent
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://scholar.google.com/',
        }
        
        # Make request to Google Scholar
        response = requests.get(gscholar_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())  # For debugging
        
        # Find the citation count
        citation_div = soup.find('div', {'class': "gs_fl gs_flb"})
        if citation_div:
            for a in citation_div.find_all('a'):
                # print(a)
                if '被引用数: ' in a.text:
                    citation_count = int(a.text.split('被引用数: ')[1])
                    return citation_count
        else:
            print("No citation count found in the response")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    arxiv_url = input("Enter ArXiv paper URL: ")
    citation_count = get_google_scholar_citation(arxiv_url)
    
    if citation_count is not None:
        print(f"Citation count: {citation_count}")
    else:
        print("Could not retrieve citation count")