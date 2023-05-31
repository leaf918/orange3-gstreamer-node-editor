'''
这种方法取的不全
'''
import gi
import pandas as pd

gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init([])

reg = Gst.Registry.get()

plugins = []
print("List Available Plugins\n")
plugins_names = [x.get_name() for x in reg.get_plugin_list()]
plugins_core_names = ['capsfilter',
                      'concat',
                      'dataurisrc',
                      'downloadbuffer',
                      'fakesrc',
                      'fakesink',
                      'fdsrc',
                      'fdsink',
                      'filesrc',
                      'funnel',
                      'identity',
                      'input - selector',
                      'output - selector',
                      'queue',
                      'queue2',
                      'filesink',
                      'tee',
                      'typefind',
                      'multiqueue',
                      'valve',
                      'streamiddemux'
                      ]
for n in plugins_names:
    # print(x.get_name())
    try:
        e = Gst.ElementFactory.make(n, None)
        plugins.append({'name': n,
                        'properties': e.list_properties()
                        })
    except:
        print(">>>> %s" % n)
        pass

pd.DataFrame(plugins).to_csv("nano_gstreamer_plugins_20230518.csv")
print("End Available Plugins\n")
