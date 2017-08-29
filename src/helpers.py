import pandas as pd

def get_left_unmatched_original_documents(raw_data_df, source_df, on):
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