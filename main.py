''' Returns:
- Number of documents matched by doctor's npi
- Number of documents matched by doctor's name and full address
- Number of documents matched by practice's full adress
- Number of documents not matched
'''
from pprint import pprint

from src.matcher import Matcher

#Define constants
source_data_path = 'source_data.json'
match_file_path = 'match_file.csv'
full_address = ["street", "street_2", "city", "state", "zip"]
npi = "npi"
full_name = ["first_name", "last_name"]

if __name__ == '__main__':
    print("Running full solution")
    matcher = Matcher(full_address, npi, full_name)
    pprint(matcher.get_solution(match_file_path, source_data_path))