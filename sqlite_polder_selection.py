# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.
# bewerking threedi_result_selection.py van de ThreeDiToolbox QGis plugin

import logging
import os

from PyQt4.QtCore import Qt, QObject

from legger.views.sql_polder_selection import SQLPolderSelectionWidget

log = logging.getLogger(__name__)


class DatabaseSelection(QObject):
    """QGIS Plugin Implementation."""

    tool_name = 'sqlite_polder_selection'

    def __init__(self, iface, ts_datasource):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        QObject.__init__(self)
        self.iface = iface

        self.ts_datasource = ts_datasource


        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.icon_path = ':/plugins/ThreeDiToolbox/icon_add_datasource.png'
        self.menu_text = u'Selecteer de sql database met de hydro-objecten ????'

        self.is_active = False
        self.dialog = None

    def on_unload(self):
        """Cleanup necessary items here when dialog is closed"""

        # disconnects
        if self.dialog:
            self.dialog.close()

    def on_close_dialog(self):
        """Cleanup necessary items here when dialog is closed"""

        self.dialog.closingDialog.disconnect(self.on_close_dialog)

        self.dialog = None
        self.is_active = False

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.is_active:

            self.is_active = True

            if self.dialog is None:
                # Create the dialog (after translation) and keep reference
                self.dialog = SQLPolderSelectionWidget(
                    parent=None,
                    iface=self.iface,
                    ts_datasource=self.ts_datasource,
                    parent_class=self)

            # connect to provide cleanup on closing of dockwidget
            self.dialog.closingDialog.connect(self.on_close_dialog)

            # show the widget
            self.dialog.show()
        #else:
        #    self.dialog.setWindowState(
        #        self.dialog.windowState() & ~Qt.WindowMinimized |
        #        Qt.WindowActive)
        #    self.dialog.raise_()