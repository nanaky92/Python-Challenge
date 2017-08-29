def transform_match_file(df, fields_to_title_case, fields_to_upper_case):
    '''Change strings of certain DataFrame columns to title case and upper case'''
    for field in fields_to_upper_case:
        df[field] = df[field].apply(lambda x: x.title() if isinstance(x, str) else x)
        
    for field in fields_to_title_case:
        df[field] = df[field].apply(lambda x: x.upper() if isinstance(x, str) else x)    
