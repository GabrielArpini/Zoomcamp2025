import pandas as pd
from sqlalchemy import create_engine
import argparse
import os
import urllib.request

def dataset_download(url):
    output_file = url.split("/")[-1]
    urllib.request.urlretrieve(url,output_file)
    return output_file
    

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    gzip = params.gzip
    
    print("Downloading data...")
    file = dataset_download(url)
    print("Download completed.")
    if ".parquet" in file:
        df = pd.read_parquet(file)
    if ".csv" in file and gzip == "True":
        df = pd.read_csv(file,compression='gzip')
    if ".csv" in file and gzip == "False": 
        df = pd.read_csv(file)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    print("Connected to the postgres instance.")
    print("ingesting data...")
    df.to_sql(name=table_name,con=engine, method='multi', chunksize=100000,if_exists='append',index=False)
    print("data successfully ingested.")
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Insert CSV or parquet data to Postgres')


    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table name for postgres')
    parser.add_argument('--url', help='url of the dataset')
    parser.add_argument('--gzip', help='file is gzip or not, use True or False',default='False')

    args = parser.parse_args()
    main(args)








