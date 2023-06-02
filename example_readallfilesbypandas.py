# import csv
import zipfile
import pandas as pd
import time
import os
from datetime import datetime
import numpy as np
from privatestuff import SQL_CONNECT
import psycopg2

# Define function to convert 'c' to 0 and 'p' to 1
def convert_c_p(value):
    if value == 'c':
        return 0
    elif value == 'p':
        return 1



def GET_ALL_RF():
    """
    Retrieves all records from the 'tbill' table in the SQL database.
    
    Returns:
    - rfstuff: A list of tuples containing the fetched data from the 'tbill' table.
    
    Example usage:
    rf_data = GET_ALL_RF()
    for row in rf_data:
        print(row)
    """
    # Establish a connection to the SQL database
    cnxn = SQL_CONNECT()

    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    # SQL query to select all records from the 'tbill' table
    query = "SELECT * from tbill"

    # Execute the SQL query
    cursor.execute(query)

    # Fetch all the records from the query result
    rfstuff = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    cnxn.close()

    # Return the fetched data
    return rfstuff


def main():
    # specify the chunk size
    chunksize = 10 ** 6

    # I have my set of file I bought
    zipfileslocation = "D:\\DATA\\OPTION\\CBOE\\"

    # List all files in the directory
    all_files = os.listdir(zipfileslocation)

    # Filter the list to only .zip files
    zip_files = [file for file in all_files if file.endswith('.zip')]
    # We sort the files to make be able to load them in chronological order. It should not matter much, but what ever.
    zip_files = sorted(zip_files)

    # Subsample size
    N = 5
    sampled_files = zip_files[:N]
    
    # Get the risk-free rates so we can calculate the time-scaled log-moneyness, and bid-ask IV
    rawrf = GET_ALL_RF()
    rfeod = np.array([dtd[1] for dtd in rawrf])
    rfbdr = np.array([a[2] for a in rawrf],dtype=float)

    # loop over all 
    for file in sampled_files:
        zipped_file_path = os.path.join(zipfileslocation, file)
        with zipfile.ZipFile(zipped_file_path) as z:
            # open the csv file within the zip file
            filename = z.infolist()[0].filename
            with z.open(filename) as f:
                # read the csv file in chunks
                for chunk in pd.read_csv(f, chunksize=chunksize):
                    # process each chunk here
                    # for example, you can load each column into a list to prepare for INSERT in SQL

                    # We need to calculate the DTE                
                    # Convert date and time string column to datetime
                    chunk['date_time_dt'] = pd.to_datetime(chunk['quote_datetime'])
                    # Convert date column to datetime
                    chunk['date_dt'] = pd.to_datetime(chunk['expiration'])
                    # Calculate difference between dates
                    chunk['delta'] = chunk['date_dt'] - chunk['date_time_dt']
                    # Get number of days between dates
                    chunk['dte'] = chunk['delta'].dt.days                

                    # We need to convert the 'c' and 'p' to 0 and 1
                    # Create new column by applying the function to the original column
                    chunk['pcflag'] = chunk['option_type'].apply(convert_c_p)

                    ticker = chunk['root'].tolist()
                    dateandtime = chunk['quote_datetime'].tolist()
                    expiration = chunk['expiration'].tolist()
                    dte = chunk['dte'].tolist()
                    pcflag = chunk['pcflag'].tolist()

                    strike = chunk['strike'].tolist()
                    bidsize = chunk['bid_size'].tolist()
                    bid = chunk['bid'].tolist()
                    # bidiv = chunk['underlying_symbol'].tolist()
                    asksize = chunk['ask_size'].tolist()
                    ask = chunk['ask'].tolist()
                    # askiv = chunk['underlying_symbol'].tolist()
                    cboeiv = chunk['implied_volatility'].tolist()
                    tick_bid = chunk['underlying_bid'].tolist()
                    tick_ask = chunk['underlying_ask'].tolist()
                    tick_price = chunk['active_underlying_price'].tolist()
                    delta = chunk['delta'].tolist()
                    gamma = chunk['gamma'].tolist()
                    theta = chunk['theta'].tolist()
                    vega = chunk['vega'].tolist()
                    rho = chunk['rho'].tolist()
                    oi = chunk['open_interest'].tolist()
                    
                    tslm = chunk['underlying_symbol'].tolist()
                    # chunk.keys()
                    # Index(['underlying_symbol', 'quote_datetime', 'root', 'expiration', 'strike',
                    #     'option_type', 'open', 'high', 'low', 'close', 'trade_volume',
                    #     'bid_size', 'bid', 'ask_size', 'ask', 'underlying_bid',
                    #     'underlying_ask', 'implied_underlying_price', 'active_underlying_price',
                    #     'implied_volatility', 'delta', 'gamma', 'theta', 'vega', 'rho',
                    #     'open_interest'],
                    #     dtype='object')

                    # CREATE TABLE optionquotes (
                    # ticker VARCHAR(10),
                    # dateandtime TIMESTAMP,
                    # expiration DATE,
                    # dte INTEGER,
                    # pcflag INTEGER,
                    # strike DOUBLE PRECISION,
                    # bidsize INTEGER,
                    # bid DOUBLE PRECISION,
                    # bidiv DOUBLE PRECISION,
                    # asksize INTEGER,
                    # ask DOUBLE PRECISION,
                    # askiv DOUBLE PRECISION,
                    # cboeiv DOUBLE PRECISION,
                    # tick_bid DOUBLE PRECISION,
                    # tick_ask DOUBLE PRECISION,
                    # tick_price DOUBLE PRECISION,
                    # delta DOUBLE PRECISION,
                    # gamma DOUBLE PRECISION,
                    # theta DOUBLE PRECISION,
                    # vega DOUBLE PRECISION,
                    # rho DOUBLE PRECISION,
                    # oi INTEGER,
                    # tslm DOUBLE PRECISION

                    # size = chunk.memory_usage(deep=True).sum()
                    # print(f'Size of df: {size} bytes')
                    here=1
        pause=1
    
if __name__ == "__main__":
    main()