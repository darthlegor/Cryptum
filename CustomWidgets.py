from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

##############################################
# COLOR PALETTE AND COSTANTS
##############################################
# 0: white
# 1: light light grey (hover)
# 2: light grey (border, disabled)
# 3: dark grey (active)
# 4: yellow
# 5: dark yellow
# 6: light orange
colors = {"1": "#ebebeb", "2": "#d6d6d6", "3": "#404040", "4": "#FFF266", "5": "#F0E460", "6": "#FFD966"}

font = QFont("Calibri Light", 11)


##############################################
# SPINBOX
##############################################
class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setFont(font)


##############################################
# LABEL
##############################################
class Label(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(font)


##############################################
# TOGGLE
##############################################
class Toggle(QCheckBox):
    def __init__(self, text, parent=None):
        # basic geometric parameters definitions
        super().__init__(text, parent)
        self.switch_width = 43
        self.switch_height = 23
        self.switch_borders_radius = (self.switch_height - 1) / 2
        self.circle_diameter = 15
        self.hover_circle_diameter = 21
        self.border_thickness = 1
        self.basetext = text
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.setFixedHeight(self.switch_height + self.border_thickness)
        # self.setMaximumWidth(400)
        self.circle_in_pos = self.hover_circle_diameter - self.circle_diameter - self.border_thickness - 1
        self.circle_position = self.circle_in_pos
        self.hover_transparency = 0
        self.bg_color_value = QColor(colors["3"])
        self.animation_curve = QEasingCurve.Linear
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(self.animation_curve)
        self.animation.setDuration(200)
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)
        self.animation3 = QPropertyAnimation(self, b"hover_transparency", self)
        self.animation3.setEasingCurve(self.animation_curve)
        self.animation3.setDuration(200)

        self.stateChanged.connect(self.startAnimation)

    def enterEvent(self, event):
        self.animation_transparency(event)

    def leaveEvent(self, event):
        self.animation_transparency(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def animation_transparency(self, value):
        self.animation3.stop()
        if value:
            self.animation3.setStartValue(0)
            self.animation3.setEndValue(80)
        else:
            self.animation3.setStartValue(80)
            self.animation3.setEndValue(0)
        self.animation3.start()

    def startAnimation(self, value):
        self.animation.stop()
        self.animation2.stop()
        if value:
            self.animation.setEndValue(self.switch_width - self.circle_diameter - self.circle_in_pos)
            self.animation2.setEndValue(QColor(colors["2"]))
        else:
            self.animation.setEndValue(self.circle_in_pos)
            self.animation2.setEndValue(QColor(colors["3"]))
        self.animation.start()
        self.animation2.start()

    @Property(float)
    def circle_position(self):
        return self._circle_position

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @Property(int)
    def hover_transparency(self):
        return self._hover_transparency

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    @hover_transparency.setter
    def hover_transparency(self, val):
        self._hover_transparency = val
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(self.border_thickness)
        pen.setColor(QColor("#000000"))
        p.setPen(pen)
        p.setFont(font)
        p.drawText(self.switch_width + 10, self.switch_height / 2 + 6, self.text())
        rect = QRect(self.border_thickness, self.border_thickness, self.switch_width - 2 * self.border_thickness,
                     self.switch_height - 2 * self.border_thickness)
        if not self.isChecked():
            p.setBrush(self.bg_color_value)
            p.drawRoundedRect(rect, self.switch_borders_radius, self.switch_borders_radius)
        else:
            p.setBrush(self.bg_color_value)
            p.drawRoundedRect(rect, self.switch_borders_radius, self.switch_borders_radius)
        if self.underMouse():
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, self.hover_transparency))
            p.drawEllipse(self.circle_position - 3, self.border_thickness, self.hover_circle_diameter,
                          self.hover_circle_diameter)
        elif not self.underMouse():
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, self.hover_transparency))
            p.drawEllipse(self.circle_position - 3, self.border_thickness, self.hover_circle_diameter,
                          self.hover_circle_diameter)
        p.setPen(QColor("#000000"))
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(self.circle_position, (self.switch_height - self.circle_diameter) / 2, self.circle_diameter,
                      self.circle_diameter)


##############################################
# CHECKBOX
##############################################
class Spunta(QCheckBox):
    def __init__(self, text):
        super().__init__(text)
        self.bg_color_value = QColor(colors["3"])
        self.basetext = text
        self.border_thickness = 1
        self.cbox_height = 23
        self.cbox_radius = 21
        self.circle_diameter = 15
        self.circle_in_pos = self.cbox_radius - self.circle_diameter - self.border_thickness - 1
        self.circle_position = self.circle_in_pos
        self.setFixedHeight(self.cbox_height + self.border_thickness)
        self.hover_transparency = 0
        self.animation_curve = QEasingCurve.Linear
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)
        self.animation3 = QPropertyAnimation(self, b"hover_transparency", self)
        self.animation3.setEasingCurve(self.animation_curve)
        self.animation3.setDuration(200)

        self.stateChanged.connect(self.startAnimation)

    def enterEvent(self, event):
        self.animation_transparency(event)

    def leaveEvent(self, event):
        self.animation_transparency(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def animation_transparency(self, value):
        self.animation3.stop()
        if value:
            self.animation3.setStartValue(0)
            self.animation3.setEndValue(80)
        else:
            self.animation3.setStartValue(80)
            self.animation3.setEndValue(0)
        self.animation3.start()

    def startAnimation(self, value):
        self.animation2.stop()
        if value:
            self.animation2.setEndValue(QColor(colors["2"]))
        else:
            self.animation2.setEndValue(QColor(colors["3"]))
        self.animation2.start()

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @Property(int)
    def hover_transparency(self):
        return self._hover_transparency

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    @hover_transparency.setter
    def hover_transparency(self, val):
        self._hover_transparency = val
        self.update()

    def drawspunta(self, p):
        p.drawLine(1, self.cbox_radius / 2 + 2, self.cbox_radius / 2 + 2, self.cbox_radius + 1)
        p.drawLine(self.cbox_radius / 2 + 2, self.cbox_radius + 1, self.cbox_radius - 3, 2)

    def paintEvent(self, e):
        p = QPainter(self)
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(self.border_thickness)
        pen.setColor(QColor("#000000"))
        p.setPen(pen)
        p.setFont(font)
        p.drawText(self.cbox_radius + 10, self.cbox_radius / 2 + 6, self.basetext)
        rect = QRect(self.border_thickness + 3, (self.cbox_height - self.circle_diameter) / 2, self.circle_diameter,
                     self.circle_diameter)
        rect2 = QRect(self.border_thickness, self.border_thickness, self.cbox_radius,
                      self.cbox_radius)
        if self.isEnabled():
            if self.underMouse():
                p.setBrush(QColor(0, 0, 0, self.hover_transparency))
                p.setPen(Qt.NoPen)
                p.drawRoundedRect(rect2, 0, 0)
                p.setPen(pen)
            elif not self.underMouse():
                p.setBrush(QColor(0, 0, 0, self.hover_transparency))
                p.setPen(Qt.NoPen)
                p.drawRoundedRect(rect2, 0, 0)
                p.setPen(pen)
            p.setBrush(self.bg_color_value)
            if self.isChecked():
                p.setPen(pen)
                p.drawRoundedRect(rect, 0, 0)
                self.drawspunta(p)
            elif not self.isChecked():
                p.setPen(pen)
                p.drawRoundedRect(rect, 0, 0)
        else:
            pen.setColor(QColor(colors["3"]))
            p.setPen(pen)
            p.setFont(font)
            p.drawText(self.cbox_radius + 10, self.cbox_radius / 2 + 6, self.basetext)
            if self.isChecked():
                p.setPen(pen)
                p.drawRoundedRect(rect, 0, 0)
                self.drawspunta(p)
            elif not self.isChecked():
                p.setPen(pen)
                p.drawRoundedRect(rect, 0, 0)


##############################################
# BUTTONS
##############################################
class Button(QPushButton):
    def __init__(self, text, size_x=200, size_y=54):
        super().__init__(text)
        self.setText(text)
        self.setFixedHeight(24)
        self.setMouseTracking(True)
        self.animation_curve = QEasingCurve.Linear
        self.bg_color_value = QColor(colors["4"])
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)

    def enterEvent(self, event):
        self.backgroundAnim(event)

    def leaveEvent(self, event):
        self.backgroundAnim(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    def backgroundAnim(self, value):
        self.animation2.stop()
        if value:
            self.animation2.setEndValue(QColor(colors["5"]))
        else:
            self.animation2.setEndValue(QColor(colors["4"]))
        self.animation2.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(font)

        rect = QRect(1, 1, self.width() - 2, self.height() - 2)
        p.setPen(QColor(colors["5"]))
        if self.underMouse():
            p.setBrush(self.bg_color_value)
            p.drawRoundedRect(rect, 4, 4)
        elif not self.underMouse():
            p.setBrush(self.bg_color_value)
        p.drawRoundedRect(rect, 4, 4)
        p.setPen(QColor("#000000"))
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
        p.end()


class UtilityBtn(QPushButton):
    def __init__(self, icon, text=None, size=24):
        super().__init__()
        self.label = text
        self.image = QPixmap(icon)
        self.setFixedSize(size, size)
        self.setMouseTracking(True)
        self.animation_curve = QEasingCurve.Linear
        self.hover_transparency = 0
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.animation3 = QPropertyAnimation(self, b"hover_transparency", self)
        self.animation3.setEasingCurve(self.animation_curve)
        self.animation3.setDuration(200)

    def enterEvent(self, event):
        self.animation_transparency(event)

    def leaveEvent(self, event):
        self.animation_transparency(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Property(int)
    def hover_transparency(self):
        return self._hover_transparency

    @hover_transparency.setter
    def hover_transparency(self, val):
        self._hover_transparency = val
        self.update()

    def animation_transparency(self, value):
        self.animation3.stop()
        if value:
            self.animation3.setStartValue(0)
            self.animation3.setEndValue(50)
        else:
            self.animation3.setStartValue(50)
            self.animation3.setEndValue(0)
        self.animation3.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(QFont("Calibri Light", 12))
        rect = QRect(0, 0, self.width(), self.height())
        p.setBrush(QColor(0, 0, 0, self.hover_transparency))
        if self.underMouse():
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, self.hover_transparency))
            p.drawRoundedRect(rect, 4, 4)
        elif not self.underMouse():
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, self.hover_transparency))
            p.drawRoundedRect(rect, 4, 4)
        p.setPen(QColor("#000000"))
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawPixmap(e.rect(), self.image)
        p.end()


##############################################
# LINEEDIT
##############################################
class PasswordLineEdit(QLineEdit):
    def __init__(self, ispsw):
        super().__init__()
        self.password_shown = False
        self.ispsw = ispsw
        self.visibleIcon = QIcon("icons/icons8-eye-96")
        self.hiddenIcon = QIcon("icons/icons8-hide-96")
        if self.ispsw:
            self.setEchoMode(QLineEdit.Password)
            self.togglepasswordAction = self.addAction(self.visibleIcon, QLineEdit.TrailingPosition)
            self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)
        elif not self.ispsw:
            pass

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)


class PasswordWidget(QWidget):
    def __init__(self, text, ispsw):
        super().__init__()
        self.ispsw = ispsw
        self.setMouseTracking(True)
        self.animation_curve = QEasingCurve.Linear
        self.label = QLabel(text)
        # self.setFixedHeight(50)
        self.labelwidth = self.label.fontMetrics().boundingRect(self.label.text()).width()
        perc = self.labelwidth / self.width() * 100
        self.edit = PasswordLineEdit(self.ispsw)
        self.border_color = QColor(255, 0, 0)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label, int(perc))
        self.layout.addWidget(self.edit, (100 - perc))
        self.layout.setContentsMargins(5, 3, 1, 3)
        self.setLayout(self.layout)
        self.bg_color_value = QColor(255, 255, 255)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)
        self.setStyleSheet("QLabel {color : #404040; padding-left: 0 0px;}")

    def enterEvent(self, event):
        self.backgroundAnim(event)

    def leaveEvent(self, event):
        self.backgroundAnim(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    def backgroundAnim(self, value):
        self.animation2.stop()
        if value:
            self.animation2.setEndValue(QColor(colors["1"]))
        else:
            self.animation2.setEndValue(QColor("#ffffff"))
        self.animation2.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        base_rect = QRect(0, 4, self.width() - 2, self.edit.height() - 1)
        bord_rect = QRect(0, 0, self.label.width() + 14, self.height())
        if self.isEnabled():
            if self.underMouse():
                p.setBrush(self.bg_color_value)
            elif not self.underMouse():
                p.setBrush(self.bg_color_value)
        else:
            p.setBrush(QColor(colors["2"]))
        p.setPen(QColor(colors["2"]))
        p.drawRoundedRect(base_rect, 4, 4)
        p.setBrush(QColor(colors["4"]))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(bord_rect, 4, 4)


class DatabaseWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setMouseTracking(True)
        self.animation_curve = QEasingCurve.Linear
        self.label = QLabel(text)
        self.labelwidth = self.label.fontMetrics().boundingRect(self.label.text()).width()
        perc = self.labelwidth / self.width() * 100
        self.database = QComboBox(self)
        self.database.setPlaceholderText("Select data")
        self.border_color = QColor(255, 0, 0)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label, int(perc))
        self.layout.addWidget(self.database, (100 - perc))
        self.layout.setContentsMargins(5, 3, 5, 3)
        self.setLayout(self.layout)
        self.bg_color_value = QColor(255, 255, 255)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)
        self.animation3 = QPropertyAnimation(self, b"hover_transparency", self)
        self.animation3.setEasingCurve(self.animation_curve)
        self.animation3.setDuration(200)
        self.setStyleSheet("QLabel {color : #404040; padding-left: 0 0px;}")

    def enterEvent(self, event):
        self.backgroundAnim(event)

    def leaveEvent(self, event):
        self.backgroundAnim(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    def backgroundAnim(self, value):
        self.animation2.stop()
        if value:
            self.animation2.setEndValue(QColor("#f2f2f2"))
        else:
            self.animation2.setEndValue(QColor("#ffffff"))
        self.animation2.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        base_rect = QRect(0, 4, self.width() - 2, self.database.height() - 1)
        bord_rect = QRect(0, 0, self.label.width() + 14, self.height())
        if self.underMouse():
            p.setBrush(self.bg_color_value)
        elif not self.underMouse():
            p.setBrush(self.bg_color_value)
        p.setPen(QColor(colors["2"]))
        p.drawRoundedRect(base_rect, 4, 4)
        p.setBrush(QColor(colors["4"]))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(bord_rect, 4, 4)


class DatabaseSimpleWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setMouseTracking(True)
        self.data=QLineEdit()
        self.layout=QHBoxLayout()
        self.layout.addWidget(self.data)
        self.layout.setContentsMargins(0, 3, 0, 3)
        self.setLayout(self.layout)
        self.animation_curve = QEasingCurve.Linear
        self.border_color = QColor(255, 0, 0)
        self.bg_color_value = QColor(255, 255, 255)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)
        self.animation3 = QPropertyAnimation(self, b"hover_transparency", self)
        self.animation3.setEasingCurve(self.animation_curve)
        self.animation3.setDuration(200)
        self.setStyleSheet(open("styles.css").read())

    def enterEvent(self, event):
        self.backgroundAnim(event)

    def leaveEvent(self, event):
        self.backgroundAnim(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    def backgroundAnim(self, value):
        self.animation2.stop()
        if value:
            self.animation2.setEndValue(QColor("#f2f2f2"))
        else:
            self.animation2.setEndValue(QColor("#ffffff"))
        self.animation2.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        base_rect = QRect(1, 4, self.data.width()-2, self.data.height()-1)
        if self.underMouse():
            p.setBrush(self.bg_color_value)
        elif not self.underMouse():
            p.setBrush(self.bg_color_value)
        p.setPen(QColor(colors["2"]))
        p.drawRoundedRect(base_rect, 4, 4)
        p.end()


class PasswordSimpleWidget(QWidget):
    def __init__(self, text, ispsw):
        super().__init__()
        self.ispsw = ispsw
        self.setMouseTracking(True)
        self.animation_curve = QEasingCurve.Linear
        self.edit = PasswordLineEdit(self.ispsw)
        self.edit.setPlaceholderText(text)
        self.border_color = QColor(255, 0, 0)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.edit)
        self.layout.setContentsMargins(0, 3, 0, 3)
        self.setLayout(self.layout)
        self.bg_color_value = QColor(255, 255, 255)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.animation2 = QPropertyAnimation(self, b"bg_color_value", self)
        self.animation2.setEasingCurve(self.animation_curve)
        self.animation2.setDuration(200)
        self.setStyleSheet(open("styles.css").read())

    def enterEvent(self, event):
        self.backgroundAnim(event)

    def leaveEvent(self, event):
        self.backgroundAnim(not event)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Property(QColor)
    def bg_color_value(self):
        return self._bg_color_value

    @bg_color_value.setter
    def bg_color_value(self, val):
        self._bg_color_value = val
        self.update()

    def backgroundAnim(self, value):
        self.animation2.stop()
        if value:
            self.animation2.setEndValue(QColor(colors["1"]))
        else:
            self.animation2.setEndValue(QColor("#ffffff"))
        self.animation2.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        base_rect = QRect(1, 4, self.width() - 2, self.edit.height() - 1)
        if self.isEnabled():
            if self.underMouse():
                p.setBrush(self.bg_color_value)
            elif not self.underMouse():
                p.setBrush(self.bg_color_value)
        else:
            p.setBrush(QColor(colors["2"]))
        p.setPen(QColor(colors["2"]))
        p.drawRoundedRect(base_rect, 4, 4)
