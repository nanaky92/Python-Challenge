import pandas as pd

from .extract_and_transform_json import (extract_source_data, 
    transform_source_data_unwinding_fields,
    transform_source_data_without_unwinding)
from .extract_and_transform_csv import transform_match_file


class Matcher:
    def __init__(self, full_address, npi, full_name):
        self.full_address = full_address
        self.npi = npi
        self.full_name = full_name
        self.result = {}


    def _get_left_unmatched_original_documents(self, raw_data_df, source_df, on):
        '''Return the documents from the left df that were not matched by the on'''
        merged_df = pd.merge(raw_data_df, 
                            source_df, 
                            indicator=True, 
                            how="outer", 
                            on=on)
        #choose only the elements that did not match from the raw_data_df
        not_matched_df = merged_df[merged_df['_merge'] == 'left_only']

        selected_columns = []
        column_rename_map = {} 

        for column in raw_data_df.columns:
            if column not in not_matched_df.columns:
                selected_columns.append("{}_x".format(column))
                column_rename_map["{}_x".format(column)] = column
            else:
                selected_columns.append(column)

        not_matched_df = not_matched_df[selected_columns]
        return not_matched_df.rename(columns = column_rename_map)

    def _calculate_results(self, raw_data_df, source_unwinded_df, source_not_unwinded_df):
        ''' Returns:
        - Number of documents matched by doctor's npi
        - Number of documents matched by doctor's name and full address
        - Number of documents matched by practice's full adress
        - Number of documents not matched
        '''
        
        #Get the df with the elements of the raw_data_df not matched by doctor's npi
        not_matched_by_npi_df = \
            self._get_left_unmatched_original_documents(raw_data_df, source_not_unwinded_df, on=self.npi)

        #Get the doctor matches by doctor's npi
        self.result["Npi Match"] = raw_data_df.shape[0] - not_matched_by_npi_df.shape[0]
        
        #Get the df with the elements of the raw_data_df not matched by practice's address
        not_matched_by_address_df = \
            self._get_left_unmatched_original_documents(raw_data_df, 
                                                  source_unwinded_df, 
                                                  on=self.full_address)

        #Get the practice matches by full address
        self.result["Address Match"] = raw_data_df.shape[0] - not_matched_by_address_df.shape[0]

        #Get the matches by doctor's name and practice's address
        self.result["Name And Address Match"] = \
                pd.merge(raw_data_df, 
                        source_unwinded_df, 
                        how="inner", 
                        on=self.full_name+self.full_address).shape[0]    
        #Get the number of documents that weren't matched according to any criteria
        self.result["Documents Not Matched"] = pd.merge(not_matched_by_npi_df, 
                                                   not_matched_by_address_df, 
                                                   how="inner", 
                                                   on=list(not_matched_by_npi_df.columns)).shape[0]

    def full_solution(self, match_file_path, source_file_path):
        ''' Returns:
        - Number of documents matched by doctor's npi
        - Number of documents matched by doctor's name and full address
        - Number of documents matched by practice's full adress
        - Number of documents not matched

        Inputs: 
        - match_file_path: path to match file (csv)
        - source_file_path: path to source file (json)
        '''
        
        # Extract and transform the source data
        source_data = extract_source_data(source_file_path)
        source_unwinded_df = transform_source_data_unwinding_fields(source_data, 
                                                                   fields_to_unwind=["practices"], 
                                                                   fields_not_to_unwind=["doctor"])
        source_not_unwinded_df = transform_source_data_without_unwinding(source_data, ["doctor"])
        
        #Extract and transform the data to match
        raw_data_df = pd.read_csv(match_file_path)
        transform_match_file(raw_data_df, 
                             fields_to_title_case = ["state"], 
                             fields_to_upper_case = ["street", "street_2", "city"])

        self._calculate_results(raw_data_df, source_unwinded_df, source_not_unwinded_df)
        return self.result
