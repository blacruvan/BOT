from typing import Tuple
from pathlib import Path
from io import StringIO
from pathlib import Path
import pandas as pd

def getStats(file) -> Tuple[str, Path]: 
    if Path(file).suffix == '.csv':
        df = pd.read_csv(file)

        #redirecciono la salida de info() al buffer por que esta funcion hace un print en vez de devolver un string
        info_buffer = StringIO()
        df.info(buf=info_buffer)

        info, stats = info_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>", ''), df.describe().to_string()
        statsFile = Path('output/stats.txt')
        with open(statsFile, 'w') as archivo:
            archivo.write(stats)

        return (info, statsFile)
    else:
        raise Exception('Unsupported file format')