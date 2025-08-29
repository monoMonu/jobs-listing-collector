import time
from .data_handler import update_output
from lib.scrapper import scrape


def main():
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


if __name__ == "__main__":
    main()
