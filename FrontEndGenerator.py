import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction, QGuiApplication, QIcon
from PySide6.QtWidgets import QSlider, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QWidget, QLabel, \
    QProgressBar, QMessageBox, QGroupBox

import BackEnd
import CustomWidgets
import AppStrings
from CustomWidgets import *

#############################################
# GLOBAL SETTINGS AND PREFERENCES INIT
#############################################
settings = QSettings("Cryptum", "Password Generator")
default_settings = AppStrings.default_settings
info_labels = {"info_symb": "ciao", "info_word": "aòlalala"}
prefs_labels = {}
try:
    cboxes_labels = AppStrings.set_language(settings.value("language"))
except:
    cboxes_labels = AppStrings.set_language(0)
    settings.setValue("language", 0)


#############################################
# DIALOG CLASSES
#############################################
class WarningDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning!")
        self.setText("At least one character set is necessary!Please chose one or more sets.")
        self.setIcon(QMessageBox.Icon.Warning)


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.max_psw_size = SpinBox()
        self.max_timer_copy = SpinBox()
        self.enable_timer = Toggle("Clipboard safety reset")
        self.max_timer_copy.setMinimum(10)
        self.max_timer_copy.setMaximum(300)
        self.max_psw_size.setMinimum(8)
        self.max_psw_size.setMaximum(50)
        try:
            self.max_psw_size.setValue(settings.value("max password size"))
            self.max_timer_copy.setValue(settings.value("max timer copy"))
            self.enable_timer.setChecked(settings.value("timer enabled"))
        except:
            self.max_psw_size.setValue(20)
            self.max_timer_copy.setValue(30)
            self.enable_timer.setChecked(True)

        self.max_psw_label = Label("Max password size:")
        self.max_timer_Label = Label("Clipboard reset timer (seconds):")

        layout = QVBoxLayout(self)
        prefs_layout = QFormLayout(self)
        prefs_layout2 = QFormLayout(self)
        prefs_layout.addRow(self.max_psw_label, self.max_psw_size)
        prefs_layout2.addRow(self.max_timer_Label, self.max_timer_copy)

        layout.addLayout(prefs_layout)
        layout.addWidget(self.enable_timer)
        layout.addLayout(prefs_layout2)

        self.restore_btn = QPushButton("Restore default")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.addButton(self.restore_btn, QDialogButtonBox.ButtonRole.ResetRole)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.enable_timer.stateChanged.connect(self.check_timer)
        self.restore_btn.clicked.connect(self.restore)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.check_timer()

    def check_timer(self):
        if self.enable_timer.isChecked():
            self.max_timer_copy.setEnabled(True)
        else:
            self.max_timer_copy.setEnabled(False)

    def restore(self):
        self.max_psw_size.setValue(20)
        self.max_timer_copy.setValue(30)
        self.enable_timer.setChecked(True)
        settings.setValue("timer enabled", int(self.enable_timer.isChecked()))
        settings.setValue("max password size", self.max_psw_size.value())
        settings.setValue("max timer copy", self.max_timer_copy.value())

    def accept(self):
        settings.setValue("max password size", self.max_psw_size.value())
        settings.setValue("max timer copy", self.max_timer_copy.value())
        settings.setValue("timer enabled", int(self.enable_timer.isChecked()))
        self.close()


class AsWordInfoDialog(QDialog):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Info")
        layout = QVBoxLayout(self)
        self.mytext = QLabel(text)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(self.mytext)
        layout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)


#############################################
# STATIC METHODS
#############################################

#############################################
# MAIN WINDOW
#############################################
class GeneratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.custom_chars = None
        self.time_timer = default_settings["max timer copy"]
        self.time = None
        self.include_space = False
        self.is_whole_word = False
        self.is_custom_included = False
        self.is_num_req = False
        self.is_case_req = False
        self.is_symb_req = False
        self.is_low_req = False
        self.auto_psw_gen = False

        self.clip = QGuiApplication.clipboard()

        self.setWindowTitle('Password Generator')
        self.setStyleSheet(open("styles.css").read())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.cmplxty_label = Label("Strength:")
        # widget declaration
        self.refr_cbox = Toggle("Auto-generate on updated settings")
        self.psw_cbox_num = Spunta("Numbers [0-9]")
        self.psw_cbox_low = Spunta(cboxes_labels["lowchar"])
        self.psw_cbox_case = Spunta("Uppercases [A-Z]")
        self.psw_cbox_symb = Spunta("ASCII Symbols")
        self.psw_view = QTextBrowser()
        self.gen_btn = Button("Generate")
        self.n_spinbox = SpinBox()
        self.erase_btn = Button("Erase")
        self.erase_btn.setIcon(QIcon("icons/icons8-erase-96.png"))
        self.copy_btn = Button("Copy")
        self.copy_btn.setIcon(QIcon("icons/icons8-copy-96.png"))
        self.cmplxty_bar = QProgressBar()
        self.safe_label = Label("Safety: N/D")
        self.n_sldr = QSlider(Qt.Orientation.Horizontal)
        self.default_btn = Button("Default")
        self.default_btn.setIcon(QIcon("icons/icons8-tune-96.png"))
        self.include_char_cbox = Toggle("Include characters or sentence")
        self.include_as_word_cbox = Spunta("As written")
        self.include_insert = PasswordWidget("Chars:",False)
        self.include_space_cbox = Spunta("Include Whitespace")
        self.include_as_word_cbox_info = UtilityBtn("None","Info",24)
        self.psw_cbox_symb_info = UtilityBtn("None","Info",24)
        self.psw_view.setFont(QFont("Arial", 24))
        font = self.psw_view.fontMetrics()
        textSize = font.size(0, self.psw_view.toPlainText())
        self.psw_view.setMaximumHeight(textSize.height() + 15)
        self.psw_view.setMinimumHeight(textSize.height() + 15)
        self.psw_cbox_low.setChecked(True)
        self.include_insert.setEnabled(False)
        self.include_space_cbox.setEnabled(False)
        self.include_as_word_cbox.setEnabled(False)
        self.n_spinbox.setValue(10)
        self.n_spinbox.setMinimum(6)
        self.cmplxty_bar.setMinimum(0)
        self.cmplxty_bar.setMaximum(100)
        self.cmplxty_bar.setFormat("%v" + " bits")
        self.n_sldr.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.n_sldr.setGeometry(500, 50, 600, 50)
        self.n_sldr.setMinimum(6)
        self.n_sldr.setValue(10)
        self.n_sldr.setSingleStep(1)
        self.n_sldr.setMinimumWidth(500)
        self.n_sldr.setMinimumHeight(50)
        try:
            self.n_spinbox.setMaximum(settings.value("max password size"))
            self.n_sldr.setMaximum(settings.value("max password size"))
            self.include_insert.setMaxLength(settings.value("max password size"))
        except:
            self.n_spinbox.setMaximum(20)
            self.n_sldr.setMaximum(20)
            self.include_insert.edit.setMaxLength(20)
        # main parent layout definition
        outer_layout = QVBoxLayout()
        # top settings group build
        top_settings_layout = QHBoxLayout()
        top_sett_group = QGroupBox()
        top_sett_group.setLayout(top_settings_layout)
        top_settings_layout.addWidget(self.refr_cbox)
        top_settings_layout.addWidget(self.default_btn)
        # password length group
        num_group = QGroupBox("Password Length:")
        num_group_layout = QHBoxLayout()
        num_group.setLayout(num_group_layout)
        num_group_layout.addWidget(self.n_sldr)
        num_group_layout.addWidget(self.n_spinbox)
        # main settings layout build
        cbox_settings_layout = QVBoxLayout()
        cbox_settings_layout2 = QHBoxLayout()
        cbox_settings_layout2.addWidget(self.psw_cbox_symb)
        cbox_settings_layout2.addWidget(self.psw_cbox_symb_info)
        cbox_set_col = QVBoxLayout()
        cbox_group = QGroupBox("Characters sets:")
        cbox_group.setLayout(cbox_set_col)
        cbox_settings_layout.addWidget(cbox_group)
        cbox_set_col.addWidget(self.psw_cbox_low)
        cbox_set_col.addWidget(self.psw_cbox_case)
        cbox_set_col.addWidget(self.psw_cbox_num)
        cbox_set_col.addLayout(cbox_settings_layout2)
        # other group build
        other_settings_layout = QVBoxLayout()
        other_settings_layout2 = QHBoxLayout()
        other_sett_group = QGroupBox("Other Settings:")
        other_settings_layout2.addWidget(self.include_as_word_cbox)
        other_settings_layout2.addWidget(self.include_as_word_cbox_info)
        other_sett_group.setLayout(other_settings_layout)
        other_settings_layout.addWidget(self.include_char_cbox)
        other_settings_layout.addWidget(self.include_insert)
        other_settings_layout.addLayout(other_settings_layout2)
        other_settings_layout.addWidget(self.include_space_cbox)
        # settings layout build
        settings_layout = QVBoxLayout()
        settings_layout2 = QHBoxLayout()
        settings_layout.addWidget(top_sett_group)
        settings_layout.addWidget(num_group)
        settings_layout2.addLayout(cbox_settings_layout, 50)
        settings_layout2.addWidget(other_sett_group, 50)
        settings_layout.addLayout(settings_layout2)
        # Password gen layout
        pasw_group = QGroupBox("Your Password:")
        pasw_layout = QVBoxLayout()
        pasw_group.setLayout(pasw_layout)
        pasw_layout.addWidget(self.psw_view)
        gen_layout = QHBoxLayout()
        gen_layout.addWidget(self.gen_btn)
        gen_layout.addWidget(self.erase_btn)
        gen_layout.addWidget(self.copy_btn)
        pasw_layout.addLayout(gen_layout)
        # complexity bar layout
        complex_layout = QHBoxLayout()
        complex_layout.addWidget(self.cmplxty_label)
        complex_layout.addWidget(self.cmplxty_bar)
        complex_layout.addWidget(self.safe_label)
        pasw_layout.addLayout(complex_layout)
        # main parent layout build
        outer_layout.addLayout(settings_layout)
        outer_layout.addWidget(pasw_group)
        self.central_widget.setLayout(outer_layout)
        # actions connected to window widgets
        self.include_as_word_cbox_info.clicked.connect(lambda text: self.showinfo(info_labels["info_word"]))
        self.psw_cbox_symb_info.clicked.connect(lambda text: self.showinfo(info_labels["info_symb"]))
        self.gen_btn.clicked.connect(self.generate)
        self.erase_btn.clicked.connect(self.erase)
        self.refr_cbox.stateChanged.connect(self.autogen)
        self.n_sldr.valueChanged.connect(self.refresh_spinbox)
        self.psw_cbox_num.stateChanged.connect(self.setup)
        self.psw_cbox_case.stateChanged.connect(self.setup)
        self.psw_cbox_symb.stateChanged.connect(self.setup)
        self.psw_cbox_low.stateChanged.connect(self.setup)
        self.n_spinbox.valueChanged.connect(self.refresh_slider)
        self.default_btn.pressed.connect(self.default_settings_reset)
        self.include_char_cbox.stateChanged.connect(self.setup)
        self.copy_btn.clicked.connect(self.copy_psw)
        self.include_insert.edit.textChanged.connect(self.verify_space)
        # create menu and status bar
        self.createMenu()
        self.statusBar().show()

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
        p4 = QPoint(0, 0)
        p.setBrush(QColor(CustomWidgets.colors["3"]))
        p.drawPolygon([p1, p2, p3, p4])

    def showinfo(self, text):
        self.info = AsWordInfoDialog(text)
        self.info.exec()

    def copy_psw(self):
        if self.psw_view.toPlainText() == "":
            self.statusBar().showMessage(
                "No password to copy", 2000)
        else:
            self.clip.setText(self.psw_view.toPlainText())
            if settings.value("timer enabled"):
                self.time_timer = settings.value("max timer copy") * 1000
                self.psw_timer = QTimer(self)
                self.psw_timer.timeout.connect(self.time_out)
                self.psw_timer.setInterval(1000)
                self.psw_timer.start()
                self.time = self.time_timer
                self.statusBar().showMessage(
                    "Password copied to clipboard, reset in " + str(int(self.time / 1000)) + " seconds")
            else:
                pass

    def time_out(self):
        self.time = self.time - 1000
        self.statusBar().showMessage(
            "Password copied to clipboard, reset in " + str(int(self.time / 1000)) + " seconds")
        if self.time == 0:
            self.clip.clear()
            self.statusBar().showMessage("Time out! Clipboard cleared", 2000)
            self.psw_timer.stop()

    # apply default settings button
    def default_settings_reset(self):
        self.psw_cbox_low.setChecked(True)
        self.psw_cbox_num.setChecked(True)
        self.psw_cbox_case.setChecked(False)
        self.psw_cbox_symb.setChecked(False)
        self.n_sldr.setValue(8)
        self.refr_cbox.setChecked(False)

    # method for "generate" button
    def generate(self):
        # verify cbox settings status
        x = self.setup()
        # generate password object
        if x == 0:
            pass
        else:
            password = BackEnd.Password(self.n_sldr.value(), self.n_sldr.maximum(), self.is_num_req,
                                                   self.is_case_req, self.is_symb_req, self.is_low_req,
                                                   self.is_custom_included, self.custom_chars, self.is_whole_word,
                                                   self.include_space)
            BackEnd.generator(password)
            # set window display values
            self.psw_view.setText(password.val)
            self.psw_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cmplxty_bar.setMaximum(int(password.max_strength))
            self.cmplxty_bar.setValue(int(password.strength))
            # set safety color
            if password.safety_color == 0:
                self.safe_label.setStyleSheet("color: red")
                self.safe_label.setText("Safety: Low")
            elif password.safety_color == 1:
                self.safe_label.setStyleSheet("color: red")
                self.safe_label.setText("Safety: Mild")
            elif password.safety_color == 2:
                self.safe_label.setStyleSheet("color: green")
                self.safe_label.setText("Safety: Good")
            elif password.safety_color == 3:
                self.safe_label.setStyleSheet("color: green")
                self.safe_label.setText("Safety: High")
            self.safe_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # method for erasing current password
    def erase(self):
        self.psw_view.setText(None)
        self.cmplxty_bar.setValue(0)
        self.safe_label.setText("Safety: N/D")
        try:
            self.psw_timer.stop()
        except:
            pass
        if self.clip.text() != "":
            self.clip.clear()
            self.statusBar().showMessage("Clipboard cleared", 2000)
        else:
            pass

    # method for autogeneration cbox
    def autogen(self):
        if self.refr_cbox.isChecked():
            self.auto_psw_gen = True
        else:
            self.auto_psw_gen = False
        return self.auto_psw_gen

    def verify_space(self):
        space = self.include_insert.edit.text().find(" ")
        if space != -1:
            self.include_space_cbox.setEnabled(True)
        else:
            self.include_space_cbox.setEnabled(False)

    def verify_cboxes(self):
        if not self.psw_cbox_low.isChecked() and not self.psw_cbox_case.isChecked() and not self.psw_cbox_num.isChecked() and not self.psw_cbox_symb.isChecked():
            verify_dialog = WarningDialog(self)
            verify_dialog.exec()
            return self.psw_cbox_low.isChecked() + self.psw_cbox_case.isChecked() + self.psw_cbox_num.isChecked() + self.psw_cbox_symb.isChecked()

    def setup(self):
        x = self.verify_cboxes()
        if self.include_char_cbox.isChecked():
            self.is_custom_included = True
            self.include_insert.setEnabled(True)
            self.include_as_word_cbox.setEnabled(True)
            self.custom_chars = self.include_insert.edit.text()
            if self.include_as_word_cbox.isChecked():
                self.is_whole_word = True
            elif not self.include_as_word_cbox.isChecked():
                self.is_whole_word = False
        elif not self.include_char_cbox.isChecked():
            self.include_insert.setEnabled(False)
            self.include_as_word_cbox.setEnabled(False)
            self.include_space_cbox.setEnabled(False)
            self.is_custom_included = False
        if self.psw_cbox_num.isChecked():
            self.is_num_req = True
        else:
            self.is_num_req = False
        if self.psw_cbox_case.isChecked():
            self.is_case_req = True
        else:
            self.is_case_req = False
        if self.psw_cbox_symb.isChecked():
            self.is_symb_req = True
        else:
            self.is_symb_req = False
        if self.psw_cbox_low.isChecked():
            self.is_low_req = True
        else:
            self.is_low_req = False
        if self.include_space_cbox.isChecked():
            self.include_space = True
        else:
            self.include_space = False
        return x

    def open_prefs(self):
        prefs = PreferencesDialog(self)
        prefs.exec()

    # refresh slider and custom text entry in respect to password length spinbox
    def refresh_slider(self):
        self.n_sldr.setMaximum(settings.value("max password size"))
        self.n_sldr.setValue(self.n_spinbox.value())
        self.include_insert.edit.setMaxLength(self.n_spinbox.value())
        if self.auto_psw_gen:
            self.generate()
        else:
            pass

    # refresh spinbox and custom text entry in respect to password length slider
    def refresh_spinbox(self):
        self.n_spinbox.setMaximum(settings.value("max password size"))
        self.n_spinbox.setValue(self.n_sldr.value())
        self.include_insert.edit.setMaxLength(self.n_sldr.value())
        self.verify_cboxes()
        if self.n_sldr.value() < 8:
            self.statusBar().showMessage("Warning! A password size under 8 characters might be unsafe!", 5000)
        if self.auto_psw_gen:
            self.generate()
        else:
            pass

    def createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.help_menu = self.menuBar().addMenu("&Help")
        exit_btn = QAction('Exit', self)
        prefs_btn = QAction('Preferences', self)
        prefs_btn.triggered.connect(self.open_prefs)
        exit_btn.triggered.connect(self.close)

        self.menu.addAction(prefs_btn)
        self.menu.addAction(exit_btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GeneratorWindow()
    win.show()
    sys.exit(app.exec())
