def convertFile(file):
    import os
    filename = os.path.splitext(os.path.basename(file))[0]
    extension = os.path.splitext(os.path.basename(file))[1]
    if extension=='.csv':
        csvToJSON(file)
        return f'output/{filename}.json'
    elif extension=='.json':
        JSONToCsv(file)
        return f'output/{filename}.csv'
    else:
        return None

def csvToJSON(file):
    import pandas as pd
    import os

    try:
        
        df = pd.read_csv(file) 
        file_name = os.path.splitext(os.path.basename(file))[0]
        output_path = f'output/{file_name}.json'
        
        df.to_json(output_path, orient='records', lines=True)
    except Exception as e:
        print(f'Error: {e}')

def JSONToCsv(file):
    import pandas as pd
    import os

    try:
        df = pd.read_json(file, lines=True)
        file_name = os.path.splitext(os.path.basename(file))[0]
        output_path = f'output/{file_name}.csv'
        
        df.to_csv(output_path, index=False)       
    except Exception as e:
        print(f'Error: {e}')