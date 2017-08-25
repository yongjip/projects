import ijson


def get_recent20(data_file_path, max_num=20):
    output = []
    with open(data_file_path) as file:
        parser = ijson.items(file, 'item')
        for i, row in enumerate(parser):
            output.append(row)
            if i > max_num:
                break
    return output
