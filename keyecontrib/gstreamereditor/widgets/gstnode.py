from AnyQt import QtWidgets
from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QGridLayout
from Orange.widgets import gui
from Orange.widgets.data.oweditdomain import VariableListModel
from Orange.widgets.settings import Setting
from Orange.widgets.utils.concurrent import ConcurrentWidgetMixin
from Orange.widgets.widget import Input, Output
from Orange.widgets.widget import OWWidget

from keyecontrib.gstreamereditor.util import gst_plugs_loader


class gstplugin(OWWidget, ConcurrentWidgetMixin):
    class Inputs:
        data = Input("pipeline", list, auto_summary=False)

    class Outputs:
        # selected_data = Output("Selected Images", Orange.data.Table)
        data = Output("pipeline", list, auto_summary=False)

    want_main_area = False
    resizing_enabled = False

    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "gstplugin"
    icon = "icons/plugin.svg"
    plugin_id: int = Setting(0)
    setting_property: dict = Setting({})

    def __init__(self):
        OWWidget.__init__(self)
        ConcurrentWidgetMixin.__init__(self)
        self.plugin_source_list = None
        self.ahead_nodes = []
        self.gui_properties = {}
        self.property_map = {}

        # create grid
        grid = QGridLayout()
        gui.widgetBox(self.controlArea, orientation=grid)

        # iPlugin Source
        hbox_plugins_source = gui.hBox(None)
        self.plugin_source_attr = gui.comboBox(
            widget=hbox_plugins_source,
            master=self,
            value='plugin_id',
            label='Plugin Name',
            orientation=Qt.Horizontal,
            callback=self.plugin_id_changed
        )
        grid.addWidget(hbox_plugins_source, 0, 0, 1, 2)
        #
        self.propertyBox = gui.vBox(self.controlArea, "Property")
        self.adjustSize()
        self._update_properties_list()

    @Inputs.data
    def dataset(self, data):
        self.ahead_nodes = data

    # @gui.deferred
    def commit(self):
        self.Outputs.data.send(self.ahead_nodes + [{
            'title': self.name,
            'property': self.property_map
        }])

    def property_changed(self):
        self.property_map = {}
        for gui_name in self.gui_properties:
            v = self.gui_properties[gui_name].text()
            if len(v) > 0:
                self.property_map[gui_name] = v
                self.setting_property[gui_name] = v

        #  commit change to pipeline flow.
        self.commit()

    def plugin_id_changed(self):
        # reset property setting values
        self.setting_property = {}
        for child in self.propertyBox.findChildren(QtWidgets.QWidget):
            child.close()
            child.deleteLater()
            child = None
        self.gui_properties = {}
        for prop_title in gst_plugs_loader.defaults().loc[self.plugin_id]['properties'].split(','):
            val_setting = ''
            try:
                val_setting = self.setting_property[prop_title]
            except:
                pass
            self.cur_property_lineedit = gui.lineEdit(
                self.propertyBox,
                self,
                value=val_setting,
                label=prop_title,
                callback=self.property_changed
            )
            self.gui_properties[prop_title] = self.cur_property_lineedit

        self.name = gst_plugs_loader.defaults().loc[self.plugin_id]['title']

    def run_ppl(self):
        print('execute pipeline')

    def save_localhost_plugins(self):
        print('save_localhost_plugins')

    def on_partial_result(self):
        # self.paths_queue = result.paths
        # self.previously_saved += 1
        pass

    def on_done(self):
        # assert len(result.paths) == 0
        # self.bt_save.setText("Save")
        self.reset_queue()

    def on_exception(self, ex: Exception):
        self.Error.general_error(ex)
        self.reset_queue()

    def _update_properties_list(self):
        self.plugin_source_attr.setModel(VariableListModel(gst_plugs_loader.defaults()['title']))
        self.plugin_id_changed()

    def clear(self):
        super().clear()
        self.cancel()

    def onDeleteWidget(self):
        self.shutdown()
        super().onDeleteWidget()


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(gstplugin).run()
