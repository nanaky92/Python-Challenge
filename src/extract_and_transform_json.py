import json
from pprint import pprint

import pandas as pd
from pandas.io.json import json_normalize

def extract_source_data(source_file):
    ''' Form a list of dictionaries from a file with a json doc per line''' 
    source_data = []
    with open(source_file) as f:
        for line in f:
            source_data.append(json.loads(line))
    return source_data


def get_formatted_not_unwinded_fields(source_series, fields_not_to_unwind):
    '''Form a list of lists with the path to the fields inside fields_to_unwind,
    and a dict mapping this path to the subfields 
    
    These are needed in order to use the json_normalize in pandas.io.json.
    
    Example: {"doctor": {"last_name": "Doe", "first_name": "John"}} will return
    -not_unwinded_fields_path = [["doctor", "first_name"], 
                                ["doctor", "last_name"]]
    -not_unwinded_naming_map = {"doctor.first_name": "first_name", 
                                "doctor.last_name": "last_name"}'''
    not_unwinded_fields_path = []
    not_unwinded_naming_map = {}
    for field in source_series:
        if field in fields_not_to_unwind:
            for subfield in source_series[field]:
                not_unwinded_fields_path.append([field, subfield])
                not_unwinded_naming_map["{}.{}".format(field, subfield)] = subfield
    return not_unwinded_fields_path, not_unwinded_naming_map

def transform_source_data_unwinding_fields(source_data, fields_to_unwind, fields_not_to_unwind):
    '''Form a DataFrame from a list of dictionaries. 
    Rename columns to follow name conventions as the csv'''
    if len(source_data) != 0:
        not_unwinded_fields_path, not_unwinded_naming_map = \
            get_formatted_not_unwinded_fields(source_data[0], fields_not_to_unwind)
    else:
        return None
    return json_normalize(source_data, 
                         fields_to_unwind, 
                         not_unwinded_fields_path).rename(
                             columns = not_unwinded_naming_map)


def transform_source_data_without_unwinding(source_data, fields_not_to_unwind):
    '''Form a DataFrame from a list of dictionaries. 
    Rename columns to follow name conventions as the csv'''
    if len(source_data) != 0:
        not_unwinded_naming_map = \
            get_formatted_not_unwinded_fields(source_data[0], fields_not_to_unwind)[1]
    else:
        return None
    
    return json_normalize(source_data).rename(
        columns = not_unwinded_naming_map)
