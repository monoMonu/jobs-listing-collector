import time
from .data_handler import update_output
from lib.scrapper import scrape
import schedule


def scheduled_run():
  schedule.every().day.at("07:00").do(update_json_data)

  while True:
    schedule.run_pending()
    time.sleep(1)


def update_json_data():
    start_time = time.perf_counter()
    data = scrape(
        type="internships", 
        role=[
            "backend-development", 
            "front-end-development", 
            "full-stack-development", 
            "software-development", 
            "web-development"
        ], 
        location="delhi", 
        stipend="",
        post_time=["Just now", "Today", "Few hours ago"]
    )
    end_time = time.perf_counter()
    if data:
        update_output(data)
    print(f"Scraping Execution Time: {end_time - start_time:.6f} seconds")


def main():
    update_json_data()
    # scheduled_run()

if __name__ == "__main__":
    main()
