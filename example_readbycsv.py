import csv
import zipfile

# specify the chunk size
chunksize = 10 ** 6

zipfilelocation = "D:\\DATA\\OPTION\\CBOE\\UnderlyingOptionsIntervals_3600sec_calcs_oi_2012-01-03.zip"
csvfilelocation = "UnderlyingOptionsIntervals_3600sec_calcs_oi_2012-01-03.csv"

# open the zipped file
with zipfile.ZipFile(zipfilelocation) as z:
    # open the csv file within the zip file
    with z.open(csvfilelocation) as f:
        # create a csv reader object
        reader = csv.reader(f)
        # read the header row
        header = next(reader)
        # initialize a list to store the current chunk
        chunk = []
        # iterate over the rows in the csv file
        for i, row in enumerate(reader):
            # add the row to the current chunk
            chunk.append(row)
            # if the chunk size is reached, process the chunk
            if (i + 1) % chunksize == 0:
                # process the chunk here
                # for example, you can load each column into a list
                column1 = [row[0] for row in chunk]
                column2 = [row[1] for row in chunk]
                # clear the chunk
                chunk = []
        # process any remaining rows in the last chunk
        if chunk:
            column1 = [row[0] for row in chunk]
            column2 = [row[1] for row in chunk]
            
            pause=1
        pause = 2