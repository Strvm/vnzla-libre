"""VoteCounter class to count votes from a json file or a string."""

import json

CANDIDATE_INDEXES = [
    {"NICOLAS MADURO": 13},
    {"LUIS MARTINEZ": 6},
    {"JAVIER BERTUCCI": 1},
    {"JOSE BRITO": 4},
    {"ANTONIO ECARRI": 6},
    {"CLAUDIO FERMIN": 1},
    {"DANIEL CEBALLOS": 2},
    {"EDMUNDO GONZALES": 3},
    {"ENRIQUE MARQUEZ": 1},
    {"BENJAMIN RAUSSEO": 1},
]


class VoteCounter:
    """VoteCounter class to count votes from a json file or a string"""

    def count(self, json_data_file_path: str) -> dict:
        """Count votes from a json file
        Args:
            json_data_file_path: Path to the json file with the votes data
        Returns:
            A dictionary with the votes for each candidate
        """
        with open(json_data_file_path, encoding="UTF-8") as json_data_file:
            data = json.load(json_data_file)
            return self._count_votes(data)

    def count_from_string(self, data_string: str) -> dict:
        """Count votes from a string
        Args:
            data_string: String with the votes data
        Returns:
            A dictionary with the votes for each candidate
        """
        vote_data = data_string.split("!")[1]
        vote_numbers = list(map(int, vote_data.split(",")))
        votes = {candidate: 0 for candidate in self.get_candidates()}

        index = 0
        for candidate_dict in CANDIDATE_INDEXES:
            for candidate, count in candidate_dict.items():
                votes[candidate] += sum(vote_numbers[index : index + count])
                index += count

        return votes

    def _count_votes(self, data) -> dict:
        """Count votes from a list of votes data
        Args:
            data: List of votes data
        Returns:
            A dictionary with the votes for each candidate
        """
        votes = {candidate: 0 for candidate in self.get_candidates()}

        for vote in data:
            vote_data = vote["data"].split("!")[1]
            vote_numbers = list(map(int, vote_data.split(",")))

            index = 0
            for candidate_dict in CANDIDATE_INDEXES:
                for candidate, count in candidate_dict.items():
                    votes[candidate] += sum(vote_numbers[index : index + count])
                    index += count

        return votes

    @staticmethod
    def get_candidates() -> list:
        """Get the list of candidates"""
        return [list(candidate_dict.keys())[0] for candidate_dict in CANDIDATE_INDEXES]


if __name__ == "__main__":
    # Example usage
    vote_counter = VoteCounter()
    votes = vote_counter.count("outputs/qr_data.json")
    print(votes)
    total_votes = sum(votes.values())
    print(total_votes)

    # Example usage for the new method
    data_string = "150702005.02.1.0001!105,7,2,0,4,1,0,1,1,1,0,2,44,2,1,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,7,13,350,0,2!0!0"
    votes_from_string = vote_counter.count_from_string(data_string)
    print(votes_from_string)
    total_votes_from_string = sum(votes_from_string.values())
    print(total_votes_from_string)
