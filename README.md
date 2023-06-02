# CBOE Data Load

This repository contains sample code for loading CBOE LiveVol CSV data into a PostgreSQL database.

The data is read from zipped files, processed, and then loaded into the database. The code is designed to read the data in chunks to handle large files that may not fit in memory.

## Examples
Two example programs are provided: `example_readbycsv.py` and `example_readbypandas.py`. These programs demonstrate how to read the zipped CSV files using the `csv` and `pandas` libraries, respectively.

In our tests, we found that reading the data in chunks using `pandas` was significantly faster than using the `csv` library. It took about 5 seconds to read the example file with `pandas`, compared to more than 20 seconds with `csv`.
