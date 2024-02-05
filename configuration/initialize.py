def createInOut():
    import os
    
    if not os.path.exists('output'):
        os.makedirs('output')
    if not os.path.exists('input'):
        os.makedirs('input')