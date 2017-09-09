import ijson
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

# today = parse(datetime.now().strftime("%F %T +0000"))

def get_recent20(data_file_path, max_num=20):
    start_date = parse(datetime.now().strftime("%F %T +0000"))
    output = []
    print(start_date)
    with open(data_file_path) as file:
        parser = ijson.items(file, 'item')
        for i, row in enumerate(parser):
            output.append(row)
            if i > max_num:
                break
    return output
