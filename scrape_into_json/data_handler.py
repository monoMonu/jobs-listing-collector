import os
import json

file_path = "scrape_into_json/output.json"

def load_existing_data(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except (json.JSONDecodeError, OSError):
                print(f"Error loading json file.")
                return []
    return []

def generate_unique_keys(entry):
    return (
        entry.get("company_name"),
        entry.get("role"),
        entry.get("location"),
        entry.get("post_time")
    )

def generate_unique_entries(existing_data, new_data):
    existing_keys = set(generate_unique_keys(item) for item in existing_data)
    unique_new_entries = []

    for j, item in enumerate(new_data, start=len(existing_data) + 1):
        new_key = generate_unique_keys(item)
        if new_key not in existing_keys:
            item["id"] = len(existing_data)+len(unique_new_entries)+1
            unique_new_entries.append(item)

    return existing_data + unique_new_entries, len(unique_new_entries)

def update_output(new_data):
  try:
    existing_data = load_existing_data(file_path)
    updated_data, count = generate_unique_entries(existing_data, new_data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)
        print(f"New entries: {count}")
  except (OSError, Exception) as e:
      print(f"Error updating data in file: {e}")
      

