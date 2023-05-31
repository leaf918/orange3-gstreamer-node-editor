from AnyQt.QtWidgets import QGridLayout
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.concurrent import ConcurrentWidgetMixin
from Orange.widgets.widget import Input
from Orange.widgets.widget import OWWidget


class gstlaunch(OWWidget, ConcurrentWidgetMixin):
    class Inputs:
        data = Input("pipeline", list)

    want_main_area = False
    resizing_enabled = False

    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "gstlaunch"
    icon = "icons/launch.svg"
    auto_run: bool = Setting(False)

    def __init__(self):
        OWWidget.__init__(self)
        ConcurrentWidgetMixin.__init__(self)
        self.plugin_source_list = None
        self.ahead_nodes = None
        # create grid
        grid = QGridLayout()
        gui.widgetBox(self.controlArea, orientation=grid)
        # auto save
        grid.addWidget(
            gui.checkBox(
                widget=None,
                master=self,
                value="auto_run",
                label="Autorun when receiving new pipeline or settings change",
                callback=self._update_messages),
            3, 0, 1, 2)

        # buttons
        gui.button(self.buttonsArea, self, "Execute Pipeline", callback=self.run_ppl)
        gui.button(self.buttonsArea, self, "Export Localhost Plugins Database", callback=self.save_localhost_plugins)

        # self.scale_combo.setEnabled(self.use_scale)
        self.adjustSize()
        self._update_messages()

    @Inputs.data
    def dataset(self, data):
        self.ahead_nodes = data
        self.setting_changed()

    def setting_changed(self):
        """
        When any setting changes save files if auto_run.
        """
        # self.scale_combo.setEnabled(self.use_scale)
        # self.reset_queue()
        if self.auto_run:
            self.run_ppl()

    def run_ppl(self):
        print('execute pipeline')
        print('-' * 12)
        print(self.ahead_nodes)
        cmd_gstlaunch = 'gst-inspect-1.0 '
        for cell in self.ahead_nodes:
            cmd = ''
            cmd += '%s ' % cell['title']
            cmd += ' '.join(['%s=%s ' % (p, cell['property'][p]) for p in cell['property']])
            cmd += '! '
            print('>><< ',cmd)
            cmd_gstlaunch += cmd
        print(cmd_gstlaunch)

    def save_localhost_plugins(self):
        print('save_localhost_plugins')

    def on_partial_result(self):
        # self.paths_queue = result.paths
        # self.previously_saved += 1
        pass

    def on_done(self):
        self.reset_queue()

    def on_exception(self, ex: Exception):
        self.Error.general_error(ex)
        self.reset_queue()

    def _update_messages(self):
        """
        Updates messages.
        """
        # self.Error.no_file_name(
        #     shown=not self.dirname and self.auto_save)

    def clear(self):
        super().clear()
        self.cancel()

    def onDeleteWidget(self):
        self.shutdown()
        super().onDeleteWidget()


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(gstlaunch).run()
