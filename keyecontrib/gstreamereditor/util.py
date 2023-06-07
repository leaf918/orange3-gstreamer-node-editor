import os

import pandas as pd


class gst_plugs_loader():
    table_default = None

    @staticmethod
    def defaults():
        if gst_plugs_loader.table_default is None:
            pth_csv = os.path.join(os.path.split(__file__)[0], 'datas/deepstream5_gstreamer_plugins_20230529_032323_.csv')
            gst_plugs_loader.table_default = pd.read_csv(pth_csv)
        return gst_plugs_loader.table_default.sort_values('title')


if __name__ == '__main__':
    print(gst_plugs_loader.defaults())
