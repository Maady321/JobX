import requests
from bs4 import BeautifulSoup
import config

def scrape_indeed():
    """Scrape Python jobs from Indeed."""
    jobs = []
    # Search for Python jobs in Remote locations
    url = "https://www.indeed.com/jobs?q=python&l=remote"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Indeed job cards often have class 'job_seen_beacon' or 'result'
        job_cards = soup.select('.job_seen_beacon') or soup.select('.result')

        for card in job_cards:
            title_element = card.find('h2', class_='jobTitle')
            link_element = card.find('a', class_='jcs-JobTitle') or card.find('a', href=True)
            
            if title_element and link_element:
                title = title_element.get_text(strip=True)
                # Cleaning title (Indeed sometimes prefixes 'new' to titles)
                if title.lower().startswith('new'):
                    title = title[3:].strip()
                
                job_id = link_element.get('data-jk')
                full_link = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else f"https://www.indeed.com{link_element['href']}"
                
                jobs.append({
                    "title": title,
                    "link": full_link,
                    "source": "Indeed"
                })
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
        
    return jobs
