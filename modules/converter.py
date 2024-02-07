import os
import pandas as pd
from pathlib import Path

def convertFile(file):
    filepath = Path(file)
    filename = filepath.stem
    extension = filepath.suffix

    if extension == '.csv':
        csvToJSON(filepath)
        return f'output/{filename}.json'
    elif extension == '.json':
        JSONToCsv(filepath)
        return f'output/{filename}.csv'
    else:
        raise Exception('Unsupported file format')

def csvToJSON(file):
    try:
        file = Path(file)
        df = pd.read_csv(file)
        file_name = file.stem
        output_path = Path('output') / f'{file_name}.json'
        
        df.to_json(output_path, orient='records')
    except Exception as e:
        print(f'Error: {e}')

def JSONToCsv(file):
    try:
        file = Path(file)
        df = pd.read_json(file)
        file_name = file.stem
        output_path = Path('output') / f'{file_name}.csv'
        
        df.to_csv(output_path, index=False)
    except Exception as e:
        print(f'Error: {e}')