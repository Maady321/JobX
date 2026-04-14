from scrapers.internshala import fetch_internshala
from filter import is_relevant
from bot import send_job

jobs = fetch_internshala()
filtered = [job for job in jobs if is_relevant(job["title"])]

print(filtered)

for job in filtered:
    send_job(job)