import pandas as pd

from .extract_and_transform_json import (extract_source_data, 
    transform_source_data_unwinding_fields,
    transform_source_data_without_unwinding)
from .extract_and_transform_csv import transform_match_file
from .partial_solutions import (number_of_documents_not_matched_by_doctors_npi,
    number_of_documents_not_matched_by_practices_npi,
    number_of_doctor_matches_by_name_and_full_address)



def full_solution(match_file_path, source_file_path):
    ''' Returns:
    - Number of documents matched by doctor's npi
    - Number of documents matched by doctor's name and full address
    - Number of documents matched by practice's full adress
    - Number of documents not matched
    '''
    result = {}
    
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

    #Get the df with the elements of the raw_data_df not matched by doctor's npi
    not_matched_by_npi_df = \
        number_of_documents_not_matched_by_doctors_npi(raw_data_df, source_not_unwinded_df)
    #Get the doctor matches by doctor's npi
    result["Npi Match"] = raw_data_df.shape[0] - not_matched_by_npi_df.shape[0]
    
    #Get the df with the elements of the raw_data_df not matched by practice's address
    not_matched_by_address_df = \
        number_of_documents_not_matched_by_practices_npi(raw_data_df, source_unwinded_df)
    #Get the practice matches by full address
    result["Address Match"] = raw_data_df.shape[0] - not_matched_by_address_df.shape[0]

    #Get the matches by doctor's name and practice's address
    result["Name And Address Match"] = \
        number_of_doctor_matches_by_name_and_full_address(source_unwinded_df, raw_data_df)
    
    #Get the number of documents that weren't matched according to any criteria
    result["Documents Not Matched"] = pd.merge(not_matched_by_npi_df, 
                                               not_matched_by_address_df, 
                                               how="inner", 
                                               on=list(not_matched_by_npi_df.columns)).shape[0]
    return result
