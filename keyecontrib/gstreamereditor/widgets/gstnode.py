from AnyQt import QtWidgets
from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QGridLayout
from Orange.widgets import gui
from Orange.widgets.data.oweditdomain import VariableListModel
from Orange.widgets.settings import Setting
from Orange.widgets.utils.concurrent import ConcurrentWidgetMixin
from Orange.widgets.widget import Input, Output
from Orange.widgets.widget import OWWidget
from PyQt5.QtWidgets import QSizePolicy
from orangewidget.gui import VerticalScrollArea, LineEditWFocusOut

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
    setting_plugin_id: int = Setting(0)
    setting_property: dict = Setting({})
    ahead_nodes: list = Setting([])

    def __init__(self):
        OWWidget.__init__(self)
        ConcurrentWidgetMixin.__init__(self)
        self.plugin_source_list = None
        self.gui_properties = {}
        self.cur_property_values = {}

        # create grid
        grid = QGridLayout()
        gui.widgetBox(self.controlArea, orientation=grid)

        # iPlugin Source
        hbox_plugins_source = gui.hBox(None)
        self.plugin_source_attr = gui.comboBox(
            widget=hbox_plugins_source,
            master=self,
            value='setting_plugin_id',
            label='Plugin Name',
            orientation=Qt.Horizontal,
            callback=self.plugin_id_changed
        )
        grid.addWidget(hbox_plugins_source, 0, 0, 1, 2)
        # contain of property

        # scroll_area = VerticalScrollArea(self.controlArea)
        # scroll_area.setSizePolicy(QSizePolicy.MinimumExpanding,
        #                           QSizePolicy.Preferred)

        self.propertyBox = gui.vBox(self.controlArea, "Property")
        self.qf = QtWidgets.QFormLayout()
        # for i in range(4): self.qf.addRow("Property", QtWidgets.QLineEdit("x"))
        self.qsa = QtWidgets.QScrollArea()
        self.qsa.setMinimumHeight(180)
        myw = QtWidgets.QWidget()
        myw.setLayout(self.qf)
        self.qsa.setWidget(myw)
        self.propertyBox.layout().addWidget(self.qsa)
        # bottom GUI
        # gui.rubber(self.controlArea)
        # gui.auto_commit(self.buttonsArea, self, 'auto_commit', 'Apply')
        self.adjustSize()
        self._update_properties_list()

    @Inputs.data
    def dataset(self, data):
        print("input data update ", data)
        self.ahead_nodes = data if data is not None else []
        self.commit()

    # @gui.deferred
    def commit(self):
        print('\n pre : %s \n cur %s \n' % (self.ahead_nodes, {
            'title': self.name,
            'property': self.cur_property_values
        }))
        self.Outputs.data.send(self.ahead_nodes + [{
            'title': self.name,
            'property': self.cur_property_values
        }])

    def property_changed(self):
        self.cur_property_values = {}
        for gui_name in self.gui_properties:
            v = self.gui_properties[gui_name].text()
            if len(v) > 0:
                self.cur_property_values[gui_name] = v
                self.setting_property[gui_name] = v

        #  commit change to pipeline flow.
        self.commit()

    def plugin_id_changed(self, from_restore=False):
        # reset property setting values
        if not from_restore:
            self.setting_property = {}
        else:
            self.ahead_nodes = []

        # for child in self.propertyBox.findChildren(QtWidgets.QWidget):
        #     child.close()
        #     child.deleteLater()
        #     child = None
        # while self.qf.count()>0:
        #     child=self.qf.takeAt(0).widget()
        #     child.close()
        #     child.deleteLater()
        #     child=None
        cur_qf = QtWidgets.QFormLayout()
        self.gui_properties = {}
        try:
            for prop_title in gst_plugs_loader.defaults().iloc[self.setting_plugin_id]['properties'].split(','):
                val_setting = ''
                try:
                    val_setting = self.setting_property[prop_title]
                except:
                    pass
                # cur_line_edit=QtWidgets.QLineEdit(val_setting)
                # print(">> qformlayout ",self.qf.count())
                cur_line_edit = LineEditWFocusOut(None,
                                                  self.property_changed,
                                                  None)
                cur_line_edit.setText(str(val_setting))

                cur_qf.addRow(prop_title,
                              cur_line_edit)
                # cur_property_lineedit = gui.lineEdit(
                #     self.propertyBox,
                #     self,
                #     value=None,
                #     label=prop_title,
                #     callback=self.property_changed
                # )
                self.gui_properties[prop_title] = cur_line_edit
                # cur_property_lineedit.setText(val_setting)
        except:
            # property may be nan
            pass
        myw = QtWidgets.QWidget()
        myw.setLayout(cur_qf)
        self.qsa.setWidget(myw)

        self.name = gst_plugs_loader.defaults().loc[self.setting_plugin_id]['title']

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
        print(" restore property ", self.setting_property, self.setting_plugin_id)
        self.plugin_source_attr.setModel(VariableListModel(gst_plugs_loader.defaults()['title']))
        # set index after setModel invoking.
        self.plugin_source_attr.setCurrentIndex(self.setting_plugin_id)
        self.plugin_id_changed(from_restore=True)

    def clear(self):
        super().clear()
        self.cancel()

    def onDeleteWidget(self):
        self.shutdown()
        super().onDeleteWidget()


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(gstplugin).run()
