import pandas as pd

def number_of_documents_not_matched_by_doctors_npi(raw_data_df, source_not_unwinded_df):
    '''Return the number of documents not matched by doctor's npi'''
    merged_by_npi_df = pd.merge(raw_data_df, 
                                source_not_unwinded_df, 
                                indicator=True, 
                                how="outer", 
                                on="npi")
    #choose only the elements that did not match from the raw_data_df
    not_matched_by_npi_df = merged_by_npi_df[merged_by_npi_df['_merge'] == 'left_only']
    selected_columns_npi_df = ["first_name_x", 
                               "last_name_x",  
                               "npi", 
                               "street", 
                               "street_2", 
                               "city", 
                               "state", 
                               "zip"]
    column_rename_map_npi_df = {"first_name_x": "first_name", 
                                "last_name_x": "last_name"}
    not_matched_by_npi_df = not_matched_by_npi_df[selected_columns_npi_df]
    return not_matched_by_npi_df.rename(columns = column_rename_map_npi_df)


def number_of_documents_not_matched_by_practices_npi(raw_data_df, source_unwinded_df):
    '''Return the number of documents not matched by practice's full address'''
    merged_by_address_df = pd.merge(raw_data_df, 
                                    source_unwinded_df, 
                                    indicator=True, 
                                    how="outer", 
                                    on=["street", "street_2", "city", "state", "zip"])
    not_matched_by_address_df = merged_by_address_df[merged_by_address_df['_merge'] == 'left_only']
    selected_columns_address_df = ["first_name_x", 
                                   "last_name_x", 
                                   "npi_x", 
                                   "street", 
                                   "street_2", 
                                   "city", 
                                   "state", 
                                   "zip"]
    column_rename_map_address_df = {"first_name_x": "first_name", 
                                    "last_name_x": "last_name", 
                                    "npi_x": "npi"}
    not_matched_by_address_df = not_matched_by_address_df[selected_columns_address_df]
    return not_matched_by_address_df.rename(columns = column_rename_map_address_df)

def number_of_doctor_matches_by_name_and_full_address(left_df, right_df):
    '''Return the number of doctor matches by 
    first_name, last_name, street, street_2, city, state and zip.
    This is done through the inner merge of two dataframes on said keys.
    The number of rows is the number of matches'''
    return pd.merge(left_df, 
                    right_df, 
                    how="inner", 
                    on=["first_name", "last_name", "street", 
                        "street_2", "city", "state", "zip"]).shape[0]
