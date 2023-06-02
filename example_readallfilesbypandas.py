# import csv
import zipfile
import pandas as pd
import time

# specify the chunk size
chunksize = 10 ** 6

# zipfilelocation = "D:\\DATA\\OPTION\\CBOE\\UnderlyingOptionsIntervals_3600sec_calcs_oi_2012-01-03.zip"
zipfilelocation = "OptionQuotes_Sample_2021-04-26.zip"

# open the zipped file
start_time = time.time()
with zipfile.ZipFile(zipfilelocation) as z:
    # open the csv file within the zip file
    filename = z.infolist()[2].filename
    with z.open(filename) as f:
        # read the csv file in chunks
        for chunk in pd.read_csv(f, chunksize=chunksize):
            # process each chunk here
            # for example, you can load each column into a list
            ticker = chunk['underlying_symbol'].tolist()
            # column2 = chunk['column2'].tolist()
            # size = chunk.memory_usage(deep=True).sum()

            # print(f'Size of df: {size} bytes')
            # here=1
end_time = time.time()
elapsed_time = end_time - start_time

print(f'Time elapsed: {elapsed_time:.2f} seconds')
pause = 1