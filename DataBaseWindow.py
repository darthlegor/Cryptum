from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QStatusBar, QDialogButtonBox

import BackEnd
import CustomWidgets
from CustomWidgets import *


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferences")


class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Entry")
        self.parent = parent
        # define widgets
        self.name = DatabaseSimpleWidget("Name:")
        self.username = DatabaseSimpleWidget("Username:")
        self.email = DatabaseSimpleWidget("email:")
        self.password = PasswordSimpleWidget("Password:", True)
        self.category = DatabaseWidget("Category")
        self.category.database.addItems(["Internet", "Misc", "Banking", "email", "Social"])
        self.use_gen_btn = UtilityBtn("icons/icons8-password-96.png", None, 24)
        self.reset_btn = UtilityBtn("icons/icons8-broom-96.png", "Clear fields", 24)
        self.autogen = UtilityBtn("icons/icons8-reset-96.png", "Generate", 24)
        # self.name.data.setPlaceholderText("Database filename")
        # define layouts
        psw_layout = QHBoxLayout()
        psw_layout.addWidget(self.name)
        psw_layout.addWidget(self.use_gen_btn)
        psw_layout.addWidget(self.reset_btn)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.email)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.category)
        self.layout.addLayout(psw_layout)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # self.buttonBox.addButton(self.reset_btn, QDialogButtonBox.ButtonRole.ResetRole)
        self.layout.addWidget(self.buttonBox)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(open("styles.css").read())
        # define actions buttons
        self.autogen.clicked.connect(self.generatepsw)
        self.reset_btn.clicked.connect(self.reset)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def generatepsw(self):
        # password auto-gen button
        password = BackEnd.Password(16, 16, True,
                                    True, True, True,
                                    False, None, False,
                                    False)
        BackEnd.generator(password)
        self.password.edit.setText(password.val)

    def accept(self):
        self.parent.database.createrow(self.parent.table.rowCount() + 1)
        tup = (self.name.data.text(), self.username.data.text(), self.email.data.text(), self.password.edit.text(),
               self.category.database.currentText())
        for i in range(len(tup)):
            self.parent.database.updatedata(self.parent.table.rowCount() + 1, i, tup[i])
        self.parent.readdata()
        self.close()

    def reset(self):
        # empty fields
        self.name.data.setText("")
        self.username.data.setText("")
        self.email.data.setText("")
        self.password.edit.setText("")


class MainWindow(QMainWindow):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.addPermanentWidget(QLabel("Version 1.0-alpha"))
        self.database = database
        self.setWindowTitle("Database -" + self.database.filename)
        self.setStyleSheet(open("styles.css").read())
        self.centralWidget = QWidget()
        out_layout = QHBoxLayout()
        self.data_list = QTreeWidget()
        self.data_list.setHeaderLabels(["Category"])
        internet = QTreeWidgetItem(self.data_list, ["Internet"])
        internet.setIcon(0, QIcon("icons/icons8-geography-96.png"))
        banking = QTreeWidgetItem(self.data_list, ["Banking"])
        banking.setIcon(0, QIcon("icons/icons8-bank-building-96.png"))
        social = QTreeWidgetItem(self.data_list, ["Social"])
        social.setIcon(0, QIcon("icons/icons8-user-account-96.png"))
        e_mail = QTreeWidgetItem(self.data_list, ["E-mails"])
        e_mail.setIcon(0, QIcon("icons/icons8-mail-96.png"))
        misc = QTreeWidgetItem(self.data_list, ["Misc"])
        misc.setIcon(0, QIcon("icons/icons8-secured-file-96.png"))
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(["Entry", "Username", "Email", "Password", "Category"])
        out_layout.addWidget(self.data_list, 30)
        out_layout.addWidget(self.table, 70)
        self.centralWidget.setLayout(out_layout)
        self.setCentralWidget(self.centralWidget)
        self.readdata()

        self.createActions()
        self.createMenu()
        self.createToolbar()
        self.statusBar().show()

    def createActions(self):
        self.new_entry_act = QAction(QIcon("icons/icons8-add-96"), "New Entry", self)
        self.edit_entry_act = QAction(QIcon("icons/icons8-edit-96"), "Edit Entry", self)
        self.remove_entry_act = QAction(QIcon("icons/icons8-cancel-96"), "Remove Entry", self)
        self.exit_act = QAction('Exit', self)
        self.lock_data_act = QAction("Lock database", self)
        self.unlock_data_act = QAction("Unlock database", self)
        self.prefs_act = QAction(QIcon("icons/icons8-settings-96.png"), "Settings", self)

        self.prefs_act.triggered.connect(self.open_prefs)
        self.exit_act.triggered.connect(self.close)
        self.new_entry_act.triggered.connect(self.newentry)
        self.remove_entry_act.triggered.connect(self.removeentry)

    def createToolbar(self):
        self.toolbar = QToolBar("Tools", self)
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.new_entry_act)
        self.toolbar.addAction(self.edit_entry_act)
        self.toolbar.addAction(self.remove_entry_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.lock_data_act)
        self.toolbar.addAction(self.unlock_data_act)

    def createMenu(self):
        self.main = self.menuBar().addMenu("&File")
        self.edit = self.menuBar().addMenu("&Edit")
        self.help_menu = self.menuBar().addMenu("&Help")

        self.main.addAction(self.prefs_act)
        self.main.addAction(self.exit_act)
        self.edit.addAction(self.new_entry_act)
        self.edit.addAction(self.edit_entry_act)
        self.edit.addAction(self.remove_entry_act)

    def readdata(self):
        self.database.openconn()
        crsr = self.database.connection.cursor()
        crsr.execute("SELECT name,username,email,password,category FROM DATA")
        self.table.setRowCount(0)
        for row, form in enumerate(crsr):
            self.table.insertRow(row)
            for column, item in enumerate(form):
                self.table.setItem(row, column, QTableWidgetItem(str(item)))
        self.database.connection.commit()
        self.database.connection.close()
        print(self.table.rowCount())
        return self.table.rowCount()

    def newentry(self):
        newdialog = NewEntryDialog(self)
        newdialog.exec()

    def removeentry(self):
        #self.table.removeRow(self.table.currentRow())
        self.database.deleterow(self.table.currentRow())
        self.readdata()

    def open_prefs(self):
        prefs = PreferencesDialog(self)
        prefs.exec()

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

    def closeEvent(self, event):
        reply = QMessageBox.warning(self, "Current database still open",
                                    "It will be crypted before app quit",
                                    QMessageBox.Ok,
                                    QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            self.database.encrypt(self.database.filename)
            event.accept()
        else:
            event.ignore()
