import os
import json
from src.selectors.fuzzy import Fuzzy
from src.helpers.get import parse_toml


if __name__ == "__main__":
    # toml path
    toml_path: str = "./config/config.toml"
    
    # parsing toml
    config = parse_toml(toml_path)

    # json_data_filepath
    json_data_filepath: str = os.path.join(config['data']['processed'], config['data']['json_output'])

    # Open the JSON file in read mode
    with open(json_data_filepath, 'r') as json_file:
        # Load JSON data from the file
        json_data = json.load(json_file)

    # Fuzzy utility
    fuzzy = Fuzzy(config, json_data)

    # source sentence
    source_sentence = "We can't predict it and we can't control it."

    # k fuzzy matches
    k_fuzzy_matches = fuzzy.get_top_k(sentence = source_sentence, k = 5)

    print(k_fuzzy_matches)
