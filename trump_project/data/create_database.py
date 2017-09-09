import json
from trumpy.etl import ETL
from trumpy.db_updater import DBUpdater


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data

raw_json_data_file_path = "raw_data_container/raw_trumps_tweets_all.json"

if __name__ == "__main__":
    raw_data = load_json(raw_json_data_file_path)

    etl = ETL()
    new_df = etl.transform(raw_data )

    updater = DBUpdater()
    updater.data = new_df.T.to_dict().values()
    updater.update_db()
