"""Combine the data from the QR code and the center data to generate the final results."""

import json

from tqdm import tqdm

from vote_counter import VoteCounter

results_data = json.loads(open("outputs/qr_data.json", encoding="UTF-8").read())
centers_data = json.loads(open("outputs/centers.json", encoding="UTF-8").read())
vote_counter = VoteCounter()
results = []


def get_center_by_image(name: str):
    """Get the center data by the image name
    Args:
        name: Name of the image
    Returns:
        The center data
    """
    for center in centers_data:
        if center["DO_DS_NAME"] == name:
            return center


for result in tqdm(results_data):
    center = get_center_by_image(result["image_path"])
    result_center = center if center else {}
    result["center"] = result_center
    votes = vote_counter.count_from_string(result["data"])
    result["votes"] = {"individual": votes, "total": sum(votes.values())}

    results.append(result)

with open("outputs/results.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(results, indent=4))
