import sys
import os
import glob

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QStatusBar, QComboBox, QDialogButtonBox, \
    QSpinBox

import BackEnd
import CustomWidgets
import DataBaseWindow
import FrontEndGenerator
from CustomWidgets import *


#############################################
# GLOBAL METHODS FOR LOGIN
#############################################

def readData(dir):
    os.chdir(dir)
    return [file for file in glob.glob("*.db")]


def filldatabox(databox):
    databox.clear()
    data = readData(os.getcwd())
    for a in range(len(data)):
        databox.addItem(data[a].replace(".db", ""))


#############################################
# CLASSES
#############################################


class WindowPars:
    def __init__(self, parent=None):
        self.win_x_size = int(app.primaryScreen().size().height() / 2)
        self.win_y_size = int(app.primaryScreen().size().width() / 3)
        self.win_x_pos = int(app.primaryScreen().size().width() / 2 - self.win_x_size / 2)
        self.win_y_pos = int(app.primaryScreen().size().height() / 2 - self.win_y_size / 2)


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.main_info = QLabel("Cryptum")
        self.info = QLabel("Version 1.0-alpha")
        self.sub_info = QLabel("Developed by Ubbabubba")
        layout = QVBoxLayout()
        layout.addWidget(self.main_info)
        layout.addWidget(self.info)
        layout.addWidget(self.sub_info)
        self.setLayout(layout)
        self.setStyleSheet(open("styles.css").read())


class PreferencesDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setlanguage = QComboBox()
        self.settimer = QSpinBox()
        layout = QVBoxLayout(self)
        self.setLayout(layout)


class NewDataDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.a = False
        self.setWindowTitle("New Database")
        # define widgets
        self.warning_label = QLabel("Attention")
        self.newdata = DatabaseSimpleWidget("Database Name:")
        self.newpsw = PasswordSimpleWidget("Master password, at least 12 chars", True)
        self.newpsw_confirm = PasswordSimpleWidget("Confirm password", True)
        self.use_gen_btn = UtilityBtn("icons/icons8-password-96.png", None, 24)
        self.reset_btn = UtilityBtn("icons/icons8-broom-96.png", "Clear fields", 24)
        self.autogen = UtilityBtn("icons/icons8-reset-96.png", "Generate", 24)
        self.newdata.data.setPlaceholderText("Database filename")
        self.newpsw_confirm.setEnabled(False)
        self.strenght = QProgressBar(self)
        # define layouts
        psw_layout = QHBoxLayout()
        psw_layout.addWidget(self.newpsw)
        psw_layout.addWidget(self.autogen)
        psw_layout.addWidget(self.use_gen_btn)
        psw_layout.addWidget(self.reset_btn)
        self.confirm_layout = QVBoxLayout()
        self.confirm_layout.addWidget(self.newpsw_confirm)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.newdata)
        self.layout.addLayout(psw_layout)
        self.layout.addLayout(self.confirm_layout)
        self.layout.addWidget(self.strenght)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # self.buttonBox.addButton(self.reset_btn, QDialogButtonBox.ButtonRole.ResetRole)
        self.layout.addWidget(self.buttonBox)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(open("styles.css").read())
        # define actions buttons
        self.newpsw.edit.textChanged.connect(self.enableconfirm)
        self.autogen.clicked.connect(self.generatepsw)
        self.reset_btn.clicked.connect(self.restore)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def generatepsw(self):
        # password auto-gen button
        password = BackEnd.Password(16, 16, True,
                                    True, True, True,
                                    False, None, False,
                                    False)
        BackEnd.generator(password)
        self.newpsw.edit.setText(password.val)

    def accept(self):
        if self.newpsw.edit.text() == "" or self.newdata.data.text() == "":
            self.warning_label.setText("Some fields are empty!")
            self.confirm_layout.addWidget(self.warning_label)
            self.a = True
        else:
            if self.newpsw.edit.text() == self.newpsw_confirm.edit.text():
                if len(self.newpsw.edit.text()) >= 6:
                    # create new database instance
                    newdata = BackEnd.DataBase(self.newdata.data.text(), False)
                    newdata.createkey(self.newpsw_confirm.edit.text(), self.newdata.data.text())
                    newdata.createdata()
                    self.close()
                    # read data files and update login combobox
                    readData(os.getcwd())
                    filldatabox(win.data_box.database)
                    self.opendatawindow(win, newdata)
                else:
                    self.warning_label.setText("Passwords too short! At least 12 chars")
                    if not self.a:
                        self.confirm_layout.addWidget(self.warning_label)
                    elif self.a:
                        pass
            else:
                self.warning_label.setText("Passwords don't match!")
                if not self.a:
                    self.confirm_layout.addWidget(self.warning_label)
                elif self.a:
                    pass

    def enableconfirm(self):
        if self.newpsw.edit.text() == "":
            self.newpsw_confirm.setEnabled(False)
        else:
            self.newpsw_confirm.setEnabled(True)

    def restore(self):
        # empty fields
        self.newdata.data.setText("")
        self.newpsw.edit.setText("")
        self.newpsw_confirm.edit.setText("")


class MainLoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.counter = 0
        self.settings = QSettings("Cryptum", "General_prefs")
        self.setWindowTitle('Cryptum')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.data_box = DatabaseWidget("Database:")
        self.login_psw_insert = PasswordWidget("Password:", True)
        self.confirm_btn = Button("Login")
        self.confirm_btn.setDefault(True)
        self.new_data_btn = UtilityBtn("icons/icons8-new-copy-96.png")
        self.new_data_btn.setStatusTip("New Database")
        self.settings_btn = UtilityBtn("icons/icons8-settings-96.png", "Go to generator", 24)
        self.info_btn = UtilityBtn("icons/icons8-info-96.png", "Go to generator", 24)
        self.gen_btn = UtilityBtn("icons/icons8-password-96.png", "Go to generator", 24)
        self.settings_btn_label = QLabel("Settings")
        self.info_btn_label = QLabel("Information")
        self.gen_btn_label = QLabel("Password Generator")

        outer_layout = QVBoxLayout()
        buttons_options_layout = QHBoxLayout()
        buttons_options_layout.addWidget(self.info_btn)
        buttons_options_layout.addWidget(self.info_btn_label)
        buttons_options_layout.addWidget(self.settings_btn)
        buttons_options_layout.addWidget(self.settings_btn_label)
        buttons_options_layout.addWidget(self.gen_btn)
        buttons_options_layout.addWidget(self.gen_btn_label)
        buttons_options_layout.setContentsMargins(50, 15, 50, 15)
        top_layout = QVBoxLayout()
        data_layout = QHBoxLayout()
        psw_layout = QHBoxLayout()
        data_layout.addWidget(self.data_box)
        data_layout.addWidget(self.new_data_btn)
        psw_layout.addWidget(self.login_psw_insert)
        top_layout.addLayout(data_layout)
        top_layout.addLayout(psw_layout)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer_layout.addLayout(top_layout)
        outer_layout.addWidget(self.confirm_btn)
        outer_layout.addLayout(buttons_options_layout)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer_layout.setContentsMargins(50, 25, 50, 25)
        self.central_widget.setLayout(outer_layout)
        self.setStyleSheet(open("styles.css").read())

        self.gen_btn.clicked.connect(self.open_generator)
        self.info_btn.clicked.connect(self.aboutinfo)
        self.settings_btn.clicked.connect(self.opensettings)
        self.new_data_btn.clicked.connect(self.newdata)
        self.confirm_btn.clicked.connect(self.verifylogin)
        self.login_psw_insert.edit.returnPressed.connect(self.verifylogin)

        filldatabox(self.data_box.database)

        self.create_status_bar()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(CustomWidgets.colors["2"]))
        p1 = QPoint(0, 0)
        p2 = QPoint(int(self.size().width()) / 8, 0)
        p3 = QPoint(int(self.size().width()) / 4, int(self.size().height()))
        p4 = QPoint(0, int(self.size().height()))
        p.drawPolygon([p1, p2, p3, p4])
        p1 = QPoint(int(self.size().width() / 2), 0)
        p2 = QPoint(int(self.size().width()), 0)
        p3 = QPoint(int(self.size().width()), int(self.size().height()))
        p4 = QPoint(int(self.size().width()) / 8, 0)
        p.setBrush(QColor(CustomWidgets.colors["3"]))
        p.drawPolygon([p1, p2, p3, p4])

    def verifylogin(self):
        filename = self.data_box.database.currentText()
        keyfilename = self.data_box.database.currentText()
        current_data = BackEnd.DataBase(filename, True)
        try:
            current_data.encryption = current_data.decrypt(keyfilename)
        except:
            self.counter = self.counter + 1
            self.status_bar.showMessage("Wrong password! " + str(3 - self.counter) + " try left", 2000)
        else:
            self.opendatawindow(current_data)
            # if self.login_psw_insert.edit.text() == "":
            #     self.status_bar.showMessage("No password inserted", 2000)
            #     pass
            # else:
            #     self.counter = self.counter + 1
            #     self.status_bar.showMessage("Wrong password! " + str(3 - self.counter) + " try left", 2000)
            #     if self.counter == 3:
            #         self.status_bar.showMessage("Login locked!", 2000)
            #         # self.lock()
            #         self.counter = 0

    def opendatawindow(self, data):
        datawin = DataBaseWindow.MainWindow(self, data)
        datawin.show()
        self.hide()

    def opensettings(self):
        settings = PreferencesDialog(self)
        settings.exec()

    def newdata(self):
        newdata_dialog = NewDataDialog(self)
        newdata_dialog.exec()

    def open_generator(self):
        self.generator = FrontEndGenerator.GeneratorWindow()
        self.generator.show()

    def aboutinfo(self):
        info_dialog = AboutDialog(self)
        info_dialog.exec()

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.addPermanentWidget(QLabel("Version 1.0-alpha"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainLoginWindow()
    win.show()
    sys.exit(app.exec())
