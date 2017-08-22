import json


def get_recent20(data_file_path):
	data_file = open(data_file_path)
	data = json.loads(data_file.read())
	
	return data[0:20]