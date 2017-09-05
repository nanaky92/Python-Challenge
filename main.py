''' Returns:
- Number of documents matched by doctor's npi
- Number of documents matched by doctor's name and full address
- Number of documents matched by practice's full adress
- Number of documents not matched
'''
from pprint import pprint

from src.matcher import Matcher

#Define constants
SOURCE_DATA_PATH = 'source_data.json'
MATCH_FILE_PATH = 'match_file.csv'
FULL_ADDRESS = ["street", "street_2", "city", "state", "zip"]
NPI = "npi"
FULL_NAME = ["first_name", "last_name"]

if __name__ == '__main__':
    print("Running full solution")
    matcher = Matcher(FULL_ADDRESS, NPI, FULL_NAME)
    pprint(matcher.get_solution(MATCH_FILE_PATH, SOURCE_DATA_PATH))