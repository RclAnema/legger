# -*- coding: utf-8 -*-
from __future__ import division

import logging
import os
import urllib2

from PyQt4.QtCore import pyqtSignal, QSettings, QModelIndex, QThread
from PyQt4.QtGui import QWidget, QFileDialog
from PyQt4 import uic

from ThreeDiToolbox.datasource.netcdf import (find_id_mapping_file, layer_qh_type_mapping)
from ThreeDiToolbox.utils.user_messages import pop_up_info


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'views','ui',
    'sql_polder_selection_dialog.ui'))

log = logging.getLogger(__name__)

class SQLPolderSelectionWidget(QWidget, FORM_CLASS):
    """Dialog for selecting model (spatialite and result files netCDFs)"""
    closingDialog = pyqtSignal()

    def __init__(
            self, parent=None, iface=None, ts_datasource=None,
            parent_class=None):
        """Constructor

        :parent: Qt parent Widget
        :iface: QGiS interface
        :ts_datasource: TimeseriesDatasourceModel instance
        :parent_class: the tool class which instantiated this widget. Is used
             here for storing volatile information
        """
        super(SQLPolderSelectionWidget, self).__init__(parent)

        self.parent_class = parent_class
        self.iface = iface
        self.setupUi(self)

        # set models on table views and update view columns
        self.ts_datasource = ts_datasource
        #self.resultTableView.setModel(self.ts_datasource)
        #self.ts_datasource.set_column_sizes_on_view(self.resultTableView)

        # connect signals
        self.selectModelSpatialiteButton.clicked.connect(
            self.select_model_spatialite_file)
        self.closeButton.clicked.connect(self.close)

    def on_close(self):
        """
        Clean object on close
        """
        self.selectTsDatasourceButton.clicked.disconnect(
            self.select_ts_datasource)
        self.closeButton.clicked.disconnect(self.close)

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """
        self.closingDialog.emit()
        self.on_close()
        event.accept()

    def model_spatialite_change(self, nr):
        """
        Change active modelsource. Called by combobox when selected
        spatialite changed
        :param nr: integer, nr of item selected in combobox
        """

        self.ts_datasource.model_spatialite_filepath = \
            self.modelSpatialiteComboBox.currentText()
        # Just emitting some dummy model indices cuz what else can we do, there
        # is no corresponding rows/columns that's been changed
        self.ts_datasource.dataChanged.emit(QModelIndex(), QModelIndex())

    def select_model_spatialite_file(self):
        """
        Open file dialog on click on button 'load model'
        :return: Boolean, if file is selected
        """

        settings = QSettings('3di', 'qgisplugin')

        try:
            init_path = settings.value('last_used_spatialite_path', type=str)
        except TypeError:
            init_path = os.path.expanduser("~")

        filename = QFileDialog.getOpenFileName(
            self,
            'Open 3Di model spatialite file',
            init_path,
            'Spatialite (*.sqlite)')

        if filename == "":
            return False

        self.ts_datasource.spatialite_filepath = filename
        index_nr = self.modelSpatialiteComboBox.findText(filename)

        if index_nr < 0:
            self.modelSpatialiteComboBox.addItem(filename)
            index_nr = self.modelSpatialiteComboBox.findText(filename)

        self.modelSpatialiteComboBox.setCurrentIndex(index_nr)

        settings.setValue('last_used_spatialite_path',
                          os.path.dirname(filename))
        return True

    @property
    def username(self):
        return self.parent_class.username

    @username.setter
    def username(self, username):
        self.parent_class.username = username

    @property
    def password(self):
        return self.parent_class.password

    @password.setter
    def password(self, password):
        self.parent_class.password = password

    @property
    def logged_in(self):
        """Return the logged in status."""
        return self.parent_class.logged_in

    def set_logged_in_status(self, username, password):
        """Set logged in status to True."""
        self.username = username
        self.password = password

    def set_logged_out_status(self):
        """Set logged in status to False."""
        self.username = None
        self.password = None
