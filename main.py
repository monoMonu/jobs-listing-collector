from bs4 import BeautifulSoup, SoupStrainer
import lxml
import requests
import json
import time

start_time = time.perf_counter()

def getUrl(role=None, location=None, page=None, stipend=None, type="jobs"):
  url = f"https://internshala.com/{type}"
  if role:
      url += f"/{role}-{type if type=="jobs" else type[:-1]}"
  if location:
      url += "/work-from-home" if location == "work-from-home" else f"/jobs-in-{location}"
  if stipend:
      url += f"/stipend-{stipend}"
  if page:
      url += f"/page-{page}"
  return url

try: 
  url = getUrl(type="internships", location="delhi", role="software-development", page=1, stipend="10000")
  print(url)
  html_doc = requests.get(url)
  html_doc.raise_for_status()

  soup = BeautifulSoup(html_doc.text, "lxml")
  only_postings = soup.select('.internship_meta.duration_meta')

  total_pages = int(soup.find(class_="page_number").select(".pagination_block.block")[-1].get_text())
  curr_page_no = 1

  data = []

  while True:

    url = getUrl(type="internships", location="delhi", role="software-development", page=curr_page_no, stipend="10000")
    html_doc = requests.get(url)
    html_doc.raise_for_status()

    soup = BeautifulSoup(html_doc.text, "lxml")
    only_postings = soup.select('.internship_meta.duration_meta')

    for i, postings in enumerate(only_postings, start=len(data)+1):
      company_name = postings.find(class_="company-name").get_text("", strip=True)
      role = postings.find(id="job_title").get_text("", strip=True)
      logo = postings.find(class_="internship_logo").find('img').get('src')
      row_1_items = postings.find_all(class_="row-1-item")
      location = row_1_items[0].find('span').get_text("", strip=True)
      stipend = row_1_items[1].find('span').get_text("", strip=True)
      duration = row_1_items[2].find('span').get_text("", strip=True)
      post_time = postings.find(class_="detail-row-2").find("span").get_text()

      data.append({
        "id": i,
        "role": role,
        "company_name": company_name,
        "logo": logo,
        "location": location,
        "stipend": stipend,
        "duration": duration,
        "post_time": post_time
      })

    if curr_page_no >= total_pages: break
    curr_page_no += 1
except Exception as e:
   print(f"Some error occurred: {e}")

with open("output.json", "a+", encoding="utf-8") as file:
  json.dump(data, file, indent=4, ensure_ascii=False)

end_time = time.perf_counter()
print(f"Execution Time: {end_time - start_time:.6f} seconds")

