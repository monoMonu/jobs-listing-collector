from bs4 import BeautifulSoup
import requests
import time
from lib.send_mail import send_email
import json


def getUrl(role, location, page, stipend, type="jobs"):
    role = ','.join(role)
    url = f"https://internshala.com/{type}"

    if type == "jobs":
        if role and location:
            url += f"/{role}-jobs-in-{location}/work-from-home"
        elif role:
            url += f"/{role}-jobs"
        elif location:
            url += f"/work-from-home/jobs-in-{location}"
    else:
        if role and location:
            url += f"/work-from-home-{role}-internships-in-{location}"
        elif role:
            url += f"/{role}-internship"
        elif location:
            url += f"/work-from-home-internships-in-{location}"

    if stipend:
        url += f"/stipend-{stipend}"
    if page:
        url += f"/page-{page}"

    return url


def scrape(role, location, stipend, page=1, type="jobs", post_time=["Just now", "Today", "Few hours ago"]):
    try: 
        data = []
        url = getUrl(role, location, page, stipend, type)
        print(url)
        html_doc = requests.get(url)
        html_doc.raise_for_status()

        soup = BeautifulSoup(html_doc.text, "lxml")
        only_postings = soup.select('.internship_meta.duration_meta')

        page_heading = soup.select("h1.page-heading")[0].get_text("", strip=True)
        print(page_heading)

        total_pages = 1
        pagination = soup.select("a.pagination_block.block")
        if pagination:
            total_pages = int(pagination[-1].get_text())
        else:
            total_pages = 1

        curr_page_no = 1

        print("total pages: ", total_pages)

        while True:
            print(f"loop-{curr_page_no}")
            url = getUrl(role, location, curr_page_no, stipend, type)
            print(f"Fetching URL: {url}")
            html_doc = requests.get(url)
            html_doc.raise_for_status()

            soup = BeautifulSoup(html_doc.text, "lxml")
            only_postings = soup.find_all(class_=['internship_meta', 'duration_meta', 'experience_meta'])
            print(f"Found {len(only_postings)} postings on page {curr_page_no}")
            
            if not only_postings:
                print(f"No postings found on page {curr_page_no}")

            for i, postings in enumerate(only_postings, start=len(data)+1):
                scrapped_post_time = postings.find(class_="detail-row-2").find("span").get_text()
                if scrapped_post_time not in set(post_time):
                    continue

                company_name = postings.find(class_="company-name").get_text("", strip=True)
                scrapped_role = postings.find(id="job_title").get_text("", strip=True)
                logo = postings.find(class_="internship_logo").find('img').get('src')
                row_1_items = postings.find_all(class_="row-1-item")
                scrapped_location = row_1_items[0].find('span').get_text("", strip=True)
                scrapped_stipend = row_1_items[1].find('span').get_text("", strip=True)
                scrapped_duration = row_1_items[2].find('span').get_text("", strip=True)
                apply_link = "https://internshala.com"+postings.parent.get("data-href")

                data.append({
                    "id": i,
                    "role": scrapped_role,
                    "company_name": company_name,
                    "logo": logo,
                    "location": scrapped_location,
                    "stipend": scrapped_stipend,
                    "duration": scrapped_duration,
                    "post_time": scrapped_post_time,
                    "apply_link": apply_link
                })

            if curr_page_no >= total_pages: break
            curr_page_no += 1

        return data

    except Exception as e:
        print(f"Some error occurred: {e}")
        send_email("Scraping Failed", f"An error occurred during scraping: {str(e)}")