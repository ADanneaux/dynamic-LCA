import pandas as pd
import numpy as np
from tqdm import tqdm

def expand_dataframe (df):

    # Identify the year columns by checking if the column names are numeric
    year_columns = [col for col in df.columns if isinstance(col, int)]

    # Initialize an empty DataFrame to store expanded data
    expanded_df = pd.DataFrame()

    # Iterate through each row in the original dataframe
    for index, row in df.iterrows():
        # Create a dictionary to hold non-year data
        expanded_row = {col: row[col] for col in df.columns if col not in year_columns}

        # Initialize an empty dictionary to hold the expanded years and values
        year_data = {}

        # Iterate through each range of five-year intervals
        for i in range(len(year_columns) - 1):
            start_year = year_columns[i]
            end_year = year_columns[i + 1]

            # Calculate the yearly increment based on the average of the five-year interval
            avg_value = (row[end_year]) / 5   

            # Assign the average for each year in the range
            for year in range(start_year + 1, end_year + 1):
                year_data[year] = avg_value


        # Combine the expanded_row and year_data to form the complete expanded row
        expanded_row.update(year_data)

        # Append the expanded_row to the expanded_df
        expanded_df = pd.concat([expanded_df, pd.DataFrame([expanded_row])], ignore_index=True)

    # Reorder the columns to ensure the years are in order
    expanded_df = expanded_df.reindex(columns=list(df.columns[:13]) + sorted([col for col in expanded_df.columns if isinstance(col, int)]))
    
    return expanded_df

def year_range (df):

    # Identify year columns starting from 2025
    year_columns = [col for col in df.columns if isinstance(col, int) and 2025 <= col < 2100]

    df = df.reindex(columns=list(df.columns[:13]) + year_columns)

    return df

def expand_dataframe_interval (df):

    # Identify the year columns by checking if the column names are numeric (integer years)
    year_columns = [col for col in df.columns if isinstance(col, int)]

    # Initialize an empty DataFrame to store the expanded data
    expanded_df = pd.DataFrame()

    # Iterate through each row in the original dataframe
    for index, row in df.iterrows():
        # Create a dictionary to hold non-year data
        expanded_row = {col: row[col] for col in df.columns if col not in year_columns}

        # Initialize an empty dictionary to hold the expanded intervals and values
        interval_data = {}

        # Iterate through the year columns and map each year to its 200 corresponding intervals
        for i, year in enumerate(year_columns):
            # Calculate start and end of the interval range
            start_interval = i * 200
            end_interval = start_interval + 199

            # Assign the same value from the year column to each interval within the range
            for interval in range(start_interval, end_interval + 1):
                interval_data[interval] = row[year]/200

        # Combine the expanded_row and interval_data to form the complete expanded row
        expanded_row.update(interval_data)

        # Append the expanded_row to the expanded_df
        expanded_df = pd.concat([expanded_df, pd.DataFrame([expanded_row])], ignore_index=True)

    # Reorder the columns to ensure the intervals are in order
    new_columns = list(df.columns[:13]) + sorted([col for col in expanded_df.columns if isinstance(col, int)])
    expanded_df = expanded_df.reindex(columns=new_columns)

    return expanded_df

def calculate_building_number(df):

    # Constants
    cf = 1e6
    area_per_capita = 30
    building_area = 1970

    # Apply the calculation to numerical columns
    numerical_columns = [col for col in df.columns if isinstance(col, int)]

    df[numerical_columns]=df[numerical_columns].apply(lambda x: (x * cf * area_per_capita) / building_area)
    
    df['Unit'] = df['Unit'].replace('million people', 'number of buildings')
    
    return df