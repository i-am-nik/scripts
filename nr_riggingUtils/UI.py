import sys
from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import shiboken2

def get_maya_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class JointCreatorUI(QtWidgets.QDialog):
    # Class-level variable to store the window instance
    _instance = None
    MIN_HEIGHT = 500
    MIN_WIDTH = 250

    def __init__(self, parent=None):
        if JointCreatorUI._instance is not None:
            JointCreatorUI._instance.close()  # Close the existing instance before creating a new one
        super(JointCreatorUI, self).__init__(parent)

        # Set window title and parent
        self.setWindowTitle("RigM8")
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMinimumHeight(self.MIN_HEIGHT)
        self.setParent(get_maya_window())  # This will keep the window inside Maya

        # Make the window movable
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        # Set layout
        self.setLayout(QtWidgets.QVBoxLayout())
        
        # Add custom title bar
        self.create_title_bar()
        
        # Create UI Elements
        self.create_ui_elements()

        # Variables to handle dragging
        self._is_dragging = False 
        self._drag_start_pos = None

        # Save the current instance
        JointCreatorUI._instance = self

    def create_title_bar(self):
        # Create a custom title bar (button for closing)
        title_bar = QtWidgets.QWidget(self)
        title_bar.setAutoFillBackground(True)
        title_bar.setStyleSheet("background-color: #333;")
        title_bar.setFixedHeight(30)

        title_layout = QtWidgets.QHBoxLayout()
        title_layout.setContentsMargins(5, 0, 5, 0)

        # Title Label
        self.title_label = QtWidgets.QLabel("RigM8 [0.0.1] Alpha")
        self.title_label.setStyleSheet("color: white;")
        title_layout.addWidget(self.title_label)

        # Minimize Button
        self.minimize_button = QtWidgets.QPushButton("_")
        self.minimize_button.setStyleSheet("background-color: #2ecc71; color: white; border: none;")
        self.minimize_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.minimize_button)

        # Close Button
        self.close_button = QtWidgets.QPushButton("X")
        self.close_button.setStyleSheet("background-color: #e74c3c; color: white; border: none;")
        self.close_button.clicked.connect(self.close)
        title_layout.addWidget(self.close_button)

        title_bar.setLayout(title_layout)

        # Add title bar to the top of the window
        self.layout().setContentsMargins(0, 5, 0, 0)  # Give space for the title bar
        self.layout().insertWidget(0, title_bar)

    def create_ui_elements(self):
        #hyperlink
        self.hyperlink_label = QtWidgets.QLabel()
        self.hyperlink_label.setText('<a href="https://www.linkedin.com/in/nikrigs/">by Nikhil Ramchandani</a>')
        self.hyperlink_label.setOpenExternalLinks(True)  # Enable opening links in the default web browser
        self.hyperlink_label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout().addWidget(self.hyperlink_label)

        # Apply updated styles
        self.apply_styles()

    def apply_styles(self):
        # Apply bold font style to all headings
        self.setStyleSheet("""
            QLabel {
                font-size: 8pt;
                font-weight: bold;
                padding: 2px;
            }
            QPushButton {
                font-size: 8pt;
                padding: 3px 3px;
                background-color: #3498db;
                color: white;
                border-radius: 3px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {
                font-size: 8pt;
                padding: 2px;
                margin: 2px;
            }
            QCheckBox {
                font-size: 8pt;
                padding: 2px;
            }
            QDialog {
                padding: 2px;
            }
        """)

    # Mouse events for dragging the window
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._is_dragging = True
            self._drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.move(event.globalPos() - self._drag_start_pos)

    def mouseReleaseEvent(self):
        self._is_dragging = False


# This will run the UI when called
def show_joint_ui():
    if JointCreatorUI._instance is None:
        window = JointCreatorUI()
        window.show()
    else:
        # If the window is already open, bring it to the front
        JointCreatorUI._instance.raise_()
        JointCreatorUI._instance.activateWindow()

# Run the UI
show_joint_ui()