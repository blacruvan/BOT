def createInOut():
    from pathlib import Path
    output, input = Path('output'), Path('input')
    if not output.exists(): output.mkdir()
    if not input.exists(): input.mkdir()

def clearOutDir():
    from pathlib import Path
    output = Path('output')
    for archivo in output.iterdir():
        if archivo.is_file():
            archivo.unlink()
            
def clearInDir():
    from pathlib import Path
    input = Path('input')
    for archivo in input.iterdir():
        if archivo.is_file():
            archivo.unlink()