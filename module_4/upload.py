import requests
import gzip
import shutil
import os
from google.cloud import storage
from google.cloud import bigquery

#https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
def download_data(n,year):
    for month in range(1, 13):
        url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{n}/{n}_tripdata_{year}-{month:02d}.csv.gz"
        gz_file = f"{n}_tripdata_{year}-{month:02d}.csv.gz"
        csv_file = f"{n}_tripdata_{year}-{month:02d}.csv"

        r = requests.get(url)
        if r.status_code == 200:
            with open(gz_file, "wb") as f:
                f.write(r.content)
            with gzip.open(gz_file, "rb") as f_in, open(csv_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(gz_file)
        print(f"Saved: {csv_file}")   

def upload_data(n,year):
    storage_client = storage.Client.from_service_account_json(
        'kestra-sandbox-449719-3c5cfbad1390.json')
    bucket = storage_client.get_bucket('week4bucketarpoca')
    for i in range(1,13):
        path = f'./{n}_tripdata_{year}-{i:02d}.csv'
        blob = bucket.blob(f'{n}_tripdata_{year}-{i:02d}.csv')
        blob.upload_from_filename(path)    
        print(f"uploaded month {i} successfully!")       

def bq_queries():  
    creds = 'kestra-sandbox-449719-3c5cfbad1390.json'
    client = bigquery.Client.from_service_account_json(json_credentials_path=creds)
    job = client.query('select * from dataset1.mytable')
def main():
    download_data('yellow','2019')
    upload_data('yellow','2019')
    
if __name__ == '__main__':
    main()
    
    
    
    
 