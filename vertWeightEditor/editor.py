import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.cmds as cmds

WINDOW_TITLE = "Skin Weight Editor"
WIDTH = 800
HEIGHT = 600
MIN_WIDTH = 300
MIN_HEIGHT = 300

def maya_main_window():
    # This function gets the main window of Maya
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class WeightEditor(QtWidgets.QDialog):
    instance = None  # Class variable to keep track of the window instance

    def __init__(self, parent=maya_main_window()):
        super(WeightEditor, self).__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WIDTH, HEIGHT)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMinimumHeight(MIN_HEIGHT)

        self.create_ui()

        # Setup scriptJob for selection change
        self.selection_job = cmds.scriptJob(event=["SelectionChanged", self.populate_joints_grid], protected=True)

        # Variables to handle dragging
        self._is_dragging = False
        self._drag_start_pos = None

        WeightEditor.instance = self  # Set the class variable to this instance

    def closeEvent(self, event):
        # Remove the scriptJob when the window is closed
        if cmds.scriptJob(exists=self.selection_job):
            cmds.scriptJob(kill=self.selection_job, force=True)
        WeightEditor.instance = None  # Clear the class variable when closed
        event.accept()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Tab widget
        self.tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.tabs)

        self.create_smooth_weight_tab()
        self.create_misc_tab()

    def create_smooth_weight_tab(self):
        # Smooth Skin Tab
        self.smooth_skin_tab = QtWidgets.QWidget()
        smooth_skin_layout = QtWidgets.QVBoxLayout(self.smooth_skin_tab)
        self.tabs.addTab(self.smooth_skin_tab, "Smooth Skin")

        joint_hold_label = QtWidgets.QLabel("Joint Hold Buttons")
        joint_hold_label.setStyleSheet("font-weight: bold;")
        smooth_skin_layout.addWidget(joint_hold_label)

        self.pre_loaded_buttons_layout = QtWidgets.QVBoxLayout()
        self.hold_buttons_layout = QtWidgets.QHBoxLayout()
        self.extra_buttons_layout = QtWidgets.QHBoxLayout()
        self.pre_loaded_buttons = []
        self.pre_loaded_buttons_names = ["Hold All", "Unhold All", "Remove Joint Weight", "Weight MinToMax"]
        self.pre_loaded_buttons_colors = ["#3498db", "#3498db", "#e74c3c", "#2ecc71"]
        
        for i in range(len(self.pre_loaded_buttons_names)):
            button = QtWidgets.QPushButton(self.pre_loaded_buttons_names[i])
            button.setStyleSheet(f"background-color: {self.pre_loaded_buttons_colors[i]}; color: white; font-size: 14px; font-weight: bold;")
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            if self.pre_loaded_buttons_names[i] == "Hold All":
                button.clicked.connect(self.hold_all_joints)
                self.hold_buttons_layout.addWidget(button)
            elif self.pre_loaded_buttons_names[i] == "Unhold All":
                button.clicked.connect(self.unhold_all_joints)
                self.hold_buttons_layout.addWidget(button)
            elif self.pre_loaded_buttons_names[i] == "Remove Joint Weight":
                button.clicked.connect(self.remove_joint_weight)
                self.extra_buttons_layout.addWidget(button)
            elif self.pre_loaded_buttons_names[i] == "Weight MinToMax":
                button.clicked.connect(self.weight_min_to_max)
                self.extra_buttons_layout.addWidget(button)
            self.pre_loaded_buttons.append(button)

        self.pre_loaded_buttons_layout.addLayout(self.hold_buttons_layout)
        self.pre_loaded_buttons_layout.addLayout(self.extra_buttons_layout)
        smooth_skin_layout.addLayout(self.pre_loaded_buttons_layout)

        self.no_selection_label = QtWidgets.QLabel("Please select the vertices")
        smooth_skin_layout.addWidget(self.no_selection_label)

        # Scroll Area for the joints buttons
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        smooth_skin_layout.addWidget(self.scroll_area)

        self.joints_grid = QtWidgets.QWidget()
        self.joints_layout = QtWidgets.QGridLayout(self.joints_grid)
        self.scroll_area.setWidget(self.joints_grid)
        self.scroll_area.setMaximumHeight(100)

        label = QtWidgets.QLabel("Smooth Skin Weights")
        label.setStyleSheet("font-weight: bold;")
        smooth_skin_layout.addWidget(label)

        self.table = QtWidgets.QTableWidget(10, 5)  # Example with 10 rows and 5 columns
        self.table.setHorizontalHeaderLabels(["Vertex", "Joint1", "Joint2", "Joint3", "Joint4"])
        smooth_skin_layout.addWidget(self.table)

        self.populate_joints_grid()

    def create_misc_tab(self):
        # Misc Tab
        self.misc_tab = QtWidgets.QWidget()
        misc_layout = QtWidgets.QVBoxLayout(self.misc_tab)
        self.tabs.addTab(self.misc_tab, "Misc")

        label = QtWidgets.QLabel("Miscellaneous Options")
        misc_layout.addWidget(label)

        reset_button = QtWidgets.QPushButton("Reset Settings")
        reset_button.clicked.connect(self.reset_settings)
        misc_layout.addWidget(reset_button)

        export_button = QtWidgets.QPushButton("Export Settings")
        export_button.clicked.connect(self.export_settings)
        misc_layout.addWidget(export_button)

    def populate_joints_grid(self, *args):
        # Clear existing buttons
        while self.joints_layout.count():
            child = self.joints_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.joint_buttons = []  # List to store joint buttons

        selected_vertices = cmds.ls(selection=True, flatten=True)
        if selected_vertices:
            joints = self.get_influencing_joints(selected_vertices)
            self.add_joint_buttons(self.joints_layout, joints)

            # Enable pre-loaded buttons and hide no selection label
            for button, color in zip(self.pre_loaded_buttons, self.pre_loaded_buttons_colors):
                button.setEnabled(True)
                button.setStyleSheet(f"background-color: {color}; color: white; font-size: 14px; font-weight: bold;")
            self.no_selection_label.hide()
        else:
            # Disable pre-loaded buttons and show no selection label
            for button, color in zip(self.pre_loaded_buttons, self.pre_loaded_buttons_colors):
                button.setEnabled(False)
                button.setStyleSheet(f"background-color: #7f8c8d; color: white; font-size: 14px; font-weight: bold;")
            self.no_selection_label.show()

    def get_influencing_joints(self, vertices):
        joints = set()
        for vertex in vertices:
            skin_cluster = cmds.ls(cmds.listHistory(vertex), type='skinCluster')
            if skin_cluster:
                influences = cmds.skinCluster(skin_cluster[0], query=True, influence=True)
                for influence in influences:
                    joints.add(influence)
        return list(joints)

    def add_joint_buttons(self, layout, joints):
        row = 0
        col = 0
        max_columns = 4 
        for joint in joints:
            button = QtWidgets.QPushButton(joint)
            button.setCheckable(True)
            button.setStyleSheet("font-size: 8px; QCheckBox::indicator:checked { background-color: green; }")
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            button.toggled.connect(lambda checked, joint_name=joint: self.set_joint_liw(joint_name, checked))
            layout.addWidget(button, row, col)
            self.joint_buttons.append(button)
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def set_joint_liw(self, joint_name, state):
        try:
            cmds.setAttr(f"{joint_name}.liw", int(state))
        except Exception as e:
            cmds.warning(f"Failed to set {joint_name}.liw: {str(e)}")

    def hold_all_joints(self):
        for button in self.joint_buttons:
            button.setChecked(True)

    def unhold_all_joints(self):
        for button in self.joint_buttons:
            button.setChecked(False)

    def reset_settings(self):
        # Placeholder for reset functionality
        pass

    def export_settings(self):
        # Placeholder for export functionality
        pass

    def remove_joint_weight(self):
        # Placeholder for remove joint weight functionality
        pass

    def weight_min_to_max(self):
        # Placeholder for weight min to max functionality
        pass

    # Mouse events for dragging the window
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._is_dragging = True
            self._drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.move(event.globalPos() - self._drag_start_pos)

    def mouseReleaseEvent(self, event):
        self._is_dragging = False

def show_weight_editor_ui():
    if WeightEditor.instance:
        WeightEditor.instance.close()  # Close the existing instance if it exists

    window = WeightEditor()
    window.show()

if __name__ == "__main__":
    show_weight_editor_ui()