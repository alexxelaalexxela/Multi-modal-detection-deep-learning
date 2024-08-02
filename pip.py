import torch
import cv2
from pathlib import Path
from matplotlib import pyplot as plt
from IPython.core.display import HTML

import deepdoctection as dd


import os

os.environ['DD_USE_TORCH'] = '1'


analyzer = dd.get_dd_analyzer(config_overwrite=["LANGUAGE='eng'"])

path = "/Users/alexandreclin/Desktop/test/report.pdf"

df = analyzer.analyze(path=path)
# This method must be called just before starting the iteration. It is part of the API.
df.reset_state()

os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/Cellar/tesseract/5.4.1/share/tessdata'

doc = iter(df)
page = next(doc)
type(page)

image = page.viz()
plt.figure(figsize=(10, 5))
plt.axis('off')
plt.imshow(image)
plt.show()
print(page.tables[0])
table = page.tables[0]
print(table.csv)
