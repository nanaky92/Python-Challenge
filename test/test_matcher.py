import unittest

import pandas as pd

from src.matcher import Matcher

class TestMatcher(unittest.TestCase):

    def test_get_solution(self):
        '''Test main method (and only public one) in Matcher class'''
        hardcoded_result = {
            'Address Match': 912,
            'Documents Not Matched': 174,
            'Name And Address Match': 912,
            'Npi Match': 864
        }
        
        #define constants
        source_data_path = 'source_data.json'
        match_file_path = 'match_file.csv'
        full_address = ["street", "street_2", "city", "state", "zip"]
        npi = "npi"
        full_name = ["first_name", "last_name"]
        
        #run matcher for solution
        matcher = Matcher(full_address, npi, full_name)
        result = matcher.get_solution(match_file_path, source_data_path)

        self.assertEqual(result, hardcoded_result)

if __name__ == '__main__':
    unittest.main()
