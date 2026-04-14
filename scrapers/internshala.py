import requests
from bs4 import BeautifulSoup

def fetch_internshala():
    url = "https://internshala.com/jobs/cyber-security-jobs/"    
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        jobs = []
        cards = soup.select(".individual_internship")

        for job in cards[:5]:
            title_tag = job.select_one("a")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = "https://internshala.com" + title_tag["href"]

            jobs.append({
                "title": title,
                "link": link,
                "source": "Internshala"
            })

        return jobs

    except Exception as e:
        print("Error in Internshala scraper:", e)
        return []
