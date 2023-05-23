from typing import Any,Generator
import pyarrow as pa
import pyarrow.parquet as pq
import csv
import pandas as pd
import os
from datetime import datetime


class UploadFiles:
    def __init__(self,file_name):
        self.file_name = file_name
        self.path='/home/guilherme/analytics/app/uploads'
        self.databases='/home/guilherme/analytics/app/databases'
        self.name = str(datetime.now()).split(" ")[0]
        
    def csv_reader(self):
        with open(self.file_name,newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            rows = [{**item} for item in reader]
            data = pd.DataFrame(rows)
         
            
            data.to_csv(os.path.join(self.path,f'excelfile-{self.name}.csv'))
        
 
    def reader_files(self):
        self.csv_reader()
        files = os.listdir(self.path)
        cont = len(files)
        i = 0
        while i < cont:
            os.path.join(self.path,files[i])
           
            df = pd.read_csv(os.path.join(self.path,files[i]),sep=",",encoding='utf-8')
            dicts = df.to_dict('records')
           
            print(dicts)
            
            
            i+=1
     
        
        #file = [file.split("\n") for file in self.csv_reader()]
        #print(file)

        #table = pa.Table.from_pandas(file)
        #print(table)
           