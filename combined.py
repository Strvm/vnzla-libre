import json

from tqdm import tqdm

from vote_counter import VoteCounter

results_data = json.loads(open("outputs/qr_data.json").read())
centers_data = json.loads(open("outputs/centers.json").read())
vote_counter = VoteCounter()
results = []


def get_center_by_image(name):
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

with open("outputs/results.json", "w") as f:
    f.write(json.dumps(results, indent=4))
