"""Combine the data from the QR code and the center data to generate the final results."""

import json
from tqdm import tqdm
from vote_counter import VoteCounter

# Load data using context managers for safety and efficiency
with open("outputs/qr_data.json", encoding="UTF-8") as qr_file:
    results_data = json.load(qr_file)

with open("outputs/centers.json", encoding="UTF-8") as centers_file:
    centers_data = json.load(centers_file)

# Initialize VoteCounter and prepare results
vote_counter = VoteCounter()
results = []

# Create a map for quick lookup of centers by acta_id
center_id_map = {
    f"{center['DO_CO_CNE_CENTER']}.0{center['DO_NU_TABLE']}": center
    for center in centers_data
    if center.get("DO_CO_CNE_CENTER") and center.get("DO_NU_TABLE")
}

# Create a map for quick lookup of centers by image name
center_name_map = {center["DO_DS_NAME"]: center for center in centers_data}


def get_center_by_acta_id(acta_id: str) -> dict:
    """Retrieve center information using acta_id."""
    key = ".".join(acta_id.split(".")[:2])
    return center_id_map.get(key, {})


def get_center_by_image(name: str) -> dict:
    """Retrieve center data using the image name."""
    return center_name_map.get(name, {})


# Process each result
for result in tqdm(results_data, desc="Processing results"):
    center = get_center_by_image(result["image_path"]) or get_center_by_acta_id(
        result["acta_id"]
    )
    result["center"] = center

    votes = vote_counter.count_from_string(result["data"])
    result["votes"] = {"individual": votes, "total": sum(votes.values())}

    results.append(result)

# Write results to JSON file
with open("outputs/results.json", "w", encoding="UTF-8") as f:
    json.dump(results, f, indent=4)
