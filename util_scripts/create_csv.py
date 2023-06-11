# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/json_to_csv.py

import os
import glob
import pandas as pd
import json.etree.ElementTree as ET

def json_to_csv(path):
    json_list = []
    for json_file in glob.glob(path + '/*.json'):
        tree = ET.parse(json_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[1][0].text),
                     int(member[1][1].text),
                     int(member[1][2].text),
                     int(member[1][3].text)
                     )
            json_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    json_df = pd.DataFrame(json_list, columns=column_name)
    return json_df

def main():
    for folder in ['train','validation']:
        image_path = os.path.join(os.getcwd(), ('images/' + folder))
        json_df = json_to_csv(image_path)
        json_df.to_csv(('images/' + folder + '_labels.csv'), index=None)
        print('Successfully converted json to csv.')

main()
