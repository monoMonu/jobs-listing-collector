from lib.send_mail import html_template, send_email
import time
from lib.scrapper import scrape

def release_mails(data):
    body = "<div>"
    for post in data:
        body += html_template.format(**post)
    body += "</div>"
    send_email(f"Job/Internship Posting Update - {len(data)} internships", body_html=body)

def main():
    start_time = time.perf_counter()
    data = scrape(
        type="internships", 
        role=["backend-development", "front-end-development", "full-stack-development", "software-development", "web-development"], 
        # role=["science"],
        location="delhi", 
        page=1, 
        stipend="1000",
        post_time=["Just now", "Today", "Few hours ago"]
    )
    if data:
        release_mails(data)
    end_time = time.perf_counter()
    print(f"Scraping Execution Time: {end_time - start_time:.6f} seconds")


if __name__ == "__main__":
    main()