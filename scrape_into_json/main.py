import time
from .data_handler import update_output
from lib.scrapper import scrape


def main():
    start_time = time.perf_counter()
    data = scrape(type="internships", role=["backend-development", "front-end-development", "full-stack-development", "software-development", "web-development"], location="delhi", page=1, stipend="")
    end_time = time.perf_counter()
    if data:
        update_output(data)
    print(f"Scraping Execution Time: {end_time - start_time:.6f} seconds")


if __name__ == "__main__":
    main()
