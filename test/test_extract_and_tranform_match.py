import unittest

from src.extract_and_transform_match import ExtractAndTransformMatch

class TestExtractAndTransformSource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nRunning test")
        cls.match_df = ExtractAndTransformMatch.extract_match_data("test/test_csv.csv")
    
    def test_extract_match_file(self):        
        columns_hardcoded = \
            set(['first_name', 'last_name', 'npi', 'street', 'street_2', 'city', 'state',  'zip'])

        self.assertEqual(set(self.match_df.columns), columns_hardcoded)
        self.assertEqual(self.match_df.shape, (2,8))
        self.assertEqual(self.match_df["first_name"][1], "Marshall")

    def test_transform_match_file(self):
        fields_to_title_case = ["state"]
        fields_to_upper_case = ["street", "street_2", "city"]

        ExtractAndTransformMatch.\
            transform_match_data(self.match_df, fields_to_title_case, fields_to_upper_case)
        
        self.assertEqual(self.match_df["state"].apply(lambda x: x.isupper()).sum(), 2)
        self.assertEqual(self.match_df["street"].apply(lambda x: x.istitle()).sum(), 2)
        self.assertEqual(self.match_df["street_2"].apply(lambda x: x.istitle()).sum(), 2)
        self.assertEqual(self.match_df["city"].apply(lambda x: x.istitle()).sum(), 2)

if __name__ == '__main__':
    unittest.main()
