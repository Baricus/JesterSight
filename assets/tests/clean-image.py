import os
from PIL import Image, ImageDraw, ImageFilter
allFiles = os.listdir(".")
baseDir = os.path.dirname(os.path.realpath(__file__))
pythonFile = os.path.basename(__file__)
for itFile in allFiles:
    if os.path.isdir(itFile):
        continue
    elif(itFile == pythonFile):
        continue
    if not itFile.endswith(('.jpg', '.png')):
        continue
    img = Image.open(itFile)
    # area = (1, 32, 1281, 752)
    area = (1, 32, (1792+1), (1008+32))
    cropped_img = img.crop(area)
    cropped_img.save('./cleaned/' + itFile.split('.')[0] + '.png')

