'''
这种方法取的不全
'''
# import gi
import subprocess
from datetime import datetime

import pandas as pd

gst_file = '/usr/bin/gst-inspect-1.0'


def get_features():
    output = subprocess.check_output([gst_file])
    lines = [line.strip() for line in output.decode().split('\n') if line.strip()]

    features = []
    for i, line in enumerate(lines):
        features.append(line.split(':')[1].strip())
    return features


def refine_property_to_json(p):
    if not p[0].startswith('Element Properties'):
        return
    title = None
    pa = []
    for i, c in enumerate(p):
        if i == 0:
            title = c
            continue
        if c.startswith('   '):
            # not property name
            continue
        pa.append(c.split(':')[0].strip())
    return pa


if __name__ == '__main__':
    objs = []
    for feature in get_features():
        try:
            if ' ' in feature:
                feature = feature.split(' ')[0]
            output = subprocess.check_output([gst_file, '%s' % feature])
        except:
            continue
        lines = [line for line in output.decode().split('\n')]

        blocks = []
        cur_info_block = []
        for line in lines:
            if len(line) == 0: continue
            if len(line) == 1 and line[0] == '\n':
                blocks.append(cur_info_block)
                cur_info_block = []
                continue
            if line[0] != ' ':
                # new block,as title
                if len(cur_info_block) > 0: blocks.append(cur_info_block)
                cur_info_block = []
                cur_info_block.append(line)  # title,
                continue
            else:
                #
                cur_info_block.append(line)  # title,content
        if len(cur_info_block) > 0:
            blocks.append(cur_info_block)
            cur_info_block = []

        ps = [refine_property_to_json(b) for b in blocks]
        ps = [p for p in ps if p is not None]
        print(feature, ps)
        objs.append({'title': feature,
                     'properties': '' if len(ps) == 0 else ','.join(ps[0])})
dsm2 = '%s_' % (datetime.now().strftime("%Y%m%d_%H%M%S"),)

pd.DataFrame(objs).to_csv(f"deepstream5_gstreamer_plugins_{dsm2}.csv")
print("End Available Plugins\n")
