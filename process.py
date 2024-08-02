from IPython.core.display import HTML
from matplotlib import pyplot as plt
import deepdoctection as dd
import os

import pandas as pd

os.environ["USE_DD_PILLOW"] = "True"
os.environ["USE_DD_OPENCV"] = "False"


def process(path):
    print(path)
    analyzer = dd.get_dd_analyzer(config_overwrite=["PT.LAYOUT.WEIGHTS=microsoft/table-transformer-detection/pytorch_model.bin",
                                  "PT.ITEM.WEIGHTS=microsoft/table-transformer-structure-recognition/pytorch_model.bin",
                                                    "PT.ITEM.FILTER=['table']",
                                                    "OCR.USE_DOCTR=True",
                                                    "OCR.USE_TESSERACT=False",
                                                    "TEXT_ORDERING.INCLUDE_RESIDUAL_TEXT_CONTAINER=True",
                                                    "TEXT_ORDERING.PARAGRAPH_BREAK=0.01",
                                                    ])

    # analyzer.pipe_component_list[0].predictor.config.threshold = 0.4  # default threshold is at 0.1

    df = analyzer.analyze(path=path)
    df.reset_state()
    df_iter = iter(df)

    dp = next(df_iter)
    np_image = dp.viz()

    plt.figure(figsize=(25, 17))
    plt.axis('off')
    plt.imshow(np_image)

    tables = dp.tables
    dataframes = []
    for table in tables:
        dataframes.append(pd.DataFrame(table.csv))

    '''dataframes = []
    for table in tables:
        data = []
        for row in table.rows:
            row_data = []
            for cell in row.bbox:  # Assume that bbox contains cell information
                row_data.append(cell)
            data.append(row_data)
        dataframes.append(pd.DataFrame(data))'''

    return dataframes


def processLayout(path, pathtext, output_image_path):

    if not os.path.exists(pathtext):
        open(pathtext, 'w').close()

    analyzer = dd.get_dd_analyzer(config_overwrite=[
                                  "PT.LAYOUT.WEIGHTS=layout/d2_model_0829999_layout_inf_only.pt"])

    df = analyzer.analyze(path=path)
    df.reset_state()
    df_iter = iter(df)

    dp = next(df_iter)
    np_image = dp.viz()

    plt.figure(figsize=(25, 17))
    plt.axis('off')
    plt.imshow(np_image)
    plt.savefig(output_image_path, format='pdf')
    layouts = dp.chunks

    with open(pathtext, 'a', encoding='utf-8') as f:  # Mode append
        for layout in layouts:
            type = layout[5]
            text = layout[6]
            if type.name == 'title':
                f.write(f'Title: {text}\n\n')
            elif type.name == 'text':
                f.write(f'Text: {text}\n\n')
            elif type.name == 'table':
                f.write(f'Table: cf the table in the exel file\n')
