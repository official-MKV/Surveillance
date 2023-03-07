import os
import cv2 as cv
import subprocess
from pathlib import Path



WDIR =Path(__file__).resolve()
parent = WDIR.parent


def convert_to_openvino(model_path):
    export_path = os.path.join(parent,'yolov5\export.py')
    args =[
        'python',
        export_path,
        '--weights',
        model_path,
        '--include',
        'openvino'
    ]
    subprocess.run(args,env=os.environ)
    #TODO: add loggings

def draw_box(img,results,color:tuple):
    for ind in results.index:
        xmin = int(results['xmin'][ind])
        ymin =int(results['ymin'][ind])
        xmax =int(results['xmax'][ind])
        ymax = int(results['ymax'][ind])
        cv.rectangle(img,(xmin,ymax),(xmax,ymin),color,2)

    return cv.cvtColor(img,cv.COLOR_RGB2BGR)


def check_for_connection():
    pass
