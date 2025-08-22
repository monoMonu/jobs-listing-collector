import os
import json

file_path = "output.json"

def load_existing_data (path):
  if(os.path.exists(path)):
    with open(file_path, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except json.JSONDecodeError:
        return []
  return []

def generate_unique_keys(entry):
  return (entry.company_name, entry.role, entry.stipend, entry.post_time)

def generate_unique_entries(past_data, new_data):
  existing_keys = set(generate_unique_keys(item) for item in past_data)

  unique_new_entries = []
  for j, item in enumerate(new_data, start=len(past_data)+1):
    if generate_unique_keys(item) not in existing_keys:
      unique_new_entries.append(item)
      item["id"] = j
    
  return past_data+unique_new_entries, len(unique_new_entries)
