import time
import asyncio
import config
import storage
import filter
import bot
from scrapers.internshala import fetch_internshala
from scrapers.indeed import scrape_indeed
from scrapers.naukri import scrape_naukri

async def job_monitoring_service():
    """Main service loop to fetch, filter, and notify about new jobs."""
    print("🚀 Job Monitoring Service Started...")
    
    seen_links = storage.load_seen()
    
    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] Starting new scrape cycle...")
        
        # 1. Gather jobs from all scrapers
        all_jobs = []
        all_jobs.extend(fetch_internshala())
        all_jobs.extend(scrape_indeed())
        all_jobs.extend(scrape_naukri())
        
        print(f"Found {len(all_jobs)} total jobs raw.")

        # 2. Filter out already seen and duplicate jobs
        unique_jobs = []
        found_links = set()
        
        for job in all_jobs:
            if job['link'] not in seen_links and job['link'] not in found_links:
                unique_jobs.append(job)
                found_links.add(job['link'])
        
        print(f"{len(unique_jobs)} new jobs to analyze.")

        # 3. Apply AI-based filtering and notify
        for job in unique_jobs:
            if filter.is_relevant(job['title']):
                print(f"✅ Relevant job found: {job['title']}")
                
                # Send Notification
                bot.send_job(job)
                
                # Update seen links
                seen_links.add(job['link'])
                storage.save_seen(seen_links)
                
                # Small delay to respect Telegram rate limits
                await asyncio.sleep(2)
            else:
                # Still mark it as seen so we don't process it again next time
                seen_links.add(job['link'])
                storage.save_seen(seen_links)

        print(f"Cycle finished. Waiting {config.SCRAPE_INTERVAL_MINUTES} minutes...")
        await asyncio.sleep(config.SCRAPE_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    try:
        asyncio.run(job_monitoring_service())
    except KeyboardInterrupt:
        print("\nStopping Job Monitoring Service...")
