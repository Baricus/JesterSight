import os
# allFiles = os.listdir(".")
allFiles = os.walk(".")
baseDir = os.path.dirname(os.path.realpath(__file__))
pythonFile = os.path.basename(__file__)

import pandas as pd

df = pd.DataFrame(columns=['file', 'crown', 'time'])

for root, dirs, files in allFiles:
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for itFile in files:
        if os.path.isdir(itFile):
            # continue
            pass
        elif(itFile == pythonFile):
            continue
        elif not itFile.endswith(('.jpg', '.png')):
            continue
        if 'no-crown' in path:
	        df = df.append({'file': '/'.join(path) + '/' + itFile, 'crown': 'false', 'time': '00:00'}, ignore_index=True)
        else:
	        df = df.append({'file': '/'.join(path) + '/' + itFile, 'crown': 'true', 'time': '00:00'}, ignore_index=True)
        # print(df)

df.to_csv(r'{}.csv'.format('tests'),index=False, header=True, mode='w')