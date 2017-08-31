import pandas as pd
import json


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


class RawTwitterDataMerger:
    def __init__(self, data=[]):
        self.data = data
        self.max_length = len(data)

    def merge(self, input_path_1, input_path_2, *args):
        part1 = load_json(input_path_1)
        part2 = load_json(input_path_2)
        if len(part1) > len(part2):
            self.max_length = len(part1)
        else:
            self.max_length = len(part2)
        merged = part1 + part2
        for path in args:
            part_i = load_json(path)
            merged += part_i
            if len(part_i) > len(self.max_length):
                self.max_length = len(part_i)
        self.data = merged
        print("Datasets Are Merged")
        print("Length of Largest Data Before Merging:", self.max_length)

    def drop_duplicates(self, dedup_by="text", sort_by="id"):
        df = pd.DataFrame(self.data, dtype='str')
        print("Length (Before Dedup):", len(df))
        print("Dropping Duplicates By", dedup_by)
        df = df.drop_duplicates(dedup_by)
        print("Length (After Dedup):", len(df))
        print("Length Of Newly Added:", len(df) - self.max_length)
        df = df.sort_values(sort_by, ascending=False)
        self.data = df
        print("DataFrame Is Sorted By", sort_by)
        print("self.data Contains DataFrame Object")

    def dump_json(self, output_path, orient="records"):
        self.data.to_json(output_path, orient=orient)
        print("Output File Orientation:", orient)
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
