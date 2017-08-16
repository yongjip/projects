import pandas as pd
import json


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


class RawTwitterDataMerger:
    def __init__(self, data=None):
        self.data = data

    def merge(self, input_path_1, input_path_2, *args):
        part1 = load_json(input_path_1)
        part2 = load_json(input_path_2)
        merged = part1 + part2
        for path in args:
            merged += load_json(path)
        self.data = merged
        print("Datasets Are Merged")
        print("Check Data Attribute.")

    def drop_duplicates(self, dedup_by="text", sort_by="id"):
        df = pd.DataFrame(self.data, dtype='str')
        df = df.drop_duplicates(dedup_by)
        df = df.sort_values(sort_by, ascending=False)
        self.data = df
        print("Dropped Duplicates by", dedup_by)
        print("Sorted by", sort_by)
        print("Data Attribute Contains DataFrame Object")

    def dump_json(self, output_path, orient="records"):
        self.data.to_json(output_path, orient=orient)
        print("Output File Orient:", orient)
        print("Check Directory:", output_path)

'''
if __name__ == "__main__":
    output_file_path = "data_container/raw_trumps_tweets_all.json"
    part1 = 'data_container/raw_trump_tweets_part_1.json'
    part2 = 'data_container/raw_trump_tweets_part_2.json'

    merger = RawTwitterDataMerger()
    merger.merge(part1, part2)
    merger.drop_duplicates()
    merger.dump_json(output_file_path)
'''
