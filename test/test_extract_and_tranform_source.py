import unittest

import pandas as pd

from src.extract_and_transform_source import ExtractAndTransformSource

class TestExtractAndTransformSource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nRunning test")
        cls.json_list = ExtractAndTransformSource.extract_source_data("test/test_json.json")
        cls.fields_to_unwind = ["practices"]
        cls.fields_not_to_unwind = ["doctor"]
    
    def test_extract_source_data(self):
        json_docs = [
                        {
                            "doctor":{
                                "first_name":"Dean",
                                "last_name":"Israel",
                                "npi":"85103080143784778415"
                            },
                            "practices":[
                                {
                                    "street":"271 Annabelle Fort",
                                    "street_2":"Apt. 404",
                                    "zip":"53549",
                                    "city":"Port Demetris",
                                    "state":"LA",
                                    "lat":"-79.8757664338564",
                                    "lon":"84.31253504872467"
                                }
                            ]
                        },
                        {
                            "doctor":{
                                "first_name":"Quinton",
                                "last_name":"Mollie",
                                "npi":"36233383542350521233"
                            },
                            "practices":[
                                {
                                    "street":"8496 Kennedi Inlet",
                                    "street_2":"Suite 815",
                                    "zip":"52665-6811",
                                    "city":"Nealville",
                                    "state":"OR",
                                    "lat":"81.37417480720865",
                                    "lon":"-95.33450729432164"
                                },
                                {
                                    "street":"29483 Nader Wall",
                                    "street_2":"Apt. 748",
                                    "zip":"46006-3437",
                                    "city":"Rashadborough",
                                    "state":"UT",
                                    "lat":"69.84837521604314",
                                    "lon":"87.36942972635728"
                                },
                                {
                                    "street":"2122 Wintheiser Valleys",
                                    "street_2":"Suite 855",
                                    "zip":"99372",
                                    "city":"South Daronland",
                                    "state":"AK",
                                    "lat":"84.90377842497296",
                                    "lon":"177.28706015725533"
                                }
                            ]
                        }
                    ]        
        self.assertEqual(self.json_list, json_docs)

    def test_transform_source_data_unwinding_fields(self):
        unwinded_df = \
            ExtractAndTransformSource.transform_source_data_unwinding_fields(
                self.json_list,
                self.fields_to_unwind,
                self.fields_not_to_unwind)

        columns_hardcoded = set(['city', 'lat', 'lon', 'state', 'street', 'street_2', 'zip', 'npi', 'first_name', 'last_name'])

        self.assertEqual(set(unwinded_df.columns), columns_hardcoded)
        self.assertEqual(unwinded_df.shape, (4,10))
        
    def test_transform_source_data_without_unwinding(self):
        not_unwinded_df = \
            ExtractAndTransformSource.transform_source_data_without_unwinding(
                self.json_list,
                self.fields_not_to_unwind)

        columns_hardcoded = set(['practices', 'npi', 'first_name', 'last_name'])

        self.assertEqual(set(not_unwinded_df.columns), columns_hardcoded)
        self.assertEqual(not_unwinded_df.shape, (2,4))

if __name__ == '__main__':
    unittest.main()
