import requests
from bs4 import BeautifulSoup
import config

def scrape_naukri():
    """Scrape Python jobs from Naukri."""
    jobs = []
    # Naukri is dynamic, but we can try to hit the search page
    # Note: Naukri often requires custom headers or Selenium for full content
    url = "https://www.naukri.com/python-jobs"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Naukri job cards typically use 'jobTuple' or similar classes
        job_cards = soup.find_all('article', class_='jobTuple') or soup.select('.srp-jobtuple-wrapper')

        for card in job_cards:
            title_element = card.find('a', class_='title')
            
            if title_element:
                title = title_element.get_text(strip=True)
                full_link = title_element['href']
                
                jobs.append({
                    "title": title,
                    "link": full_link,
                    "source": "Naukri"
                })
    except Exception as e:
        print(f"Error scraping Naukri: {e}")
        
    return jobs
