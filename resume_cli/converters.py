import csv
import json
import sys

import csv
import json
import yaml
from pathlib import Path


def convert_linkedin_to_json(input_csv, output_json):
    resume_entries = []

    try:
        with open(input_csv, mode='r', encoding='utf-8') as f:
            # LinkedIn CSVs often have a few lines of metadata at the top.
            # This skips empty lines until it finds the header.
            reader = csv.DictReader(f)

            for row in reader:
                # Mapping LinkedIn CSV headers to your YAML/JSON schema
                entry = {
                    "name": row.get("Company Name", "").strip(),
                    "position": row.get("Title", "").strip(),
                    "startDate": row.get("Started On", "").strip(),
                    "endDate": row.get("Finished On", "").strip() or "Present",
                    "summary": row.get("Description", "").strip(),
                    "highlights": []  # CSVs don't usually have bullet points separated
                }
                resume_entries.append(entry)

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(resume_entries, f, indent=2)

        print(f"Successfully converted {len(resume_entries)} entries to {output_json}")

    except FileNotFoundError:
        print(f"Error: Could not find {input_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")


def yaml_to_json(yaml_path: Path) -> str:
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    return json.dumps(data, indent=2)

def json_to_yaml(json_path: Path) -> str:
    with open(json_path, 'r') as f:
        data = json.load(f)
    return yaml.dump(data, sort_keys=False)

def linkedin_csv_to_dict(csv_path: Path):
    experience = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            experience.append({
                "name": row.get("Company Name", ""),
                "position": row.get("Title", ""),
                "startDate": row.get("Started On", ""),
                "endDate": row.get("Finished On", "") or "Present",
                "summary": row.get("Description", ""),
                "highlights": []
            })
    return {"work": experience}