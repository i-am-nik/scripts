import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QPixmap
from shiboken2 import wrapInstance
import maya.cmds as cmds

WINDOW_TITLE = "Orient Joint Tool"
MIN_WIDTH = 250
MIN_HEIGHT = 350                                                 

def maya_main_window():
    # This function gets the main window of Maya
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class OrientJoint(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(OrientJoint, self).__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMinimumHeight(MIN_HEIGHT)

        self.selected_items = []
        self.transform_choice = ""
        self.axis_selection = []

        self.create_ui()

    def create_ui(self):
        # This function sets up the user interface
        layout = QtWidgets.QVBoxLayout(self)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)

        self.note_label = QtWidgets.QLabel("Live representation of joint orientation")
        left_layout.addWidget(self.note_label)

        self.image_pixmap = QPixmap(r"E:\Repos\scripts\utils\img1.png")

        self.image_lbl = QtWidgets.QLabel()
        self.image_lbl.setPixmap(self.image_pixmap)

        self.create_btn = QtWidgets.QPushButton("Toggle Local Axes Visibility")
        self.create_btn.setStyleSheet("background-color: rgb(50, 150, 220); color: white;")
        self.create_btn.clicked.connect(self.collect_data)
        
        left_layout.addWidget(self.image_lbl)
        left_layout.addWidget(self.create_btn)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        self.world_orient_cb = QtWidgets.QCheckBox("Orient Joint to World")
        right_layout.addWidget(self.world_orient_cb)

        primary_axis_group = QtWidgets.QGroupBox("Primary Axis")
        primary_axis_layout = QtWidgets.QHBoxLayout(primary_axis_group)
        self.primary_axis_radio_grp = QtWidgets.QButtonGroup()
        self.primary_axis_radio_x = QtWidgets.QRadioButton("X")
        self.primary_axis_radio_y = QtWidgets.QRadioButton("Y")
        self.primary_axis_radio_z = QtWidgets.QRadioButton("Z")
        self.primary_axis_radio_grp.addButton(self.primary_axis_radio_x)
        self.primary_axis_radio_grp.addButton(self.primary_axis_radio_y)
        self.primary_axis_radio_grp.addButton(self.primary_axis_radio_z)
        primary_axis_layout.addWidget(self.primary_axis_radio_x)
        primary_axis_layout.addWidget(self.primary_axis_radio_y)
        primary_axis_layout.addWidget(self.primary_axis_radio_z)
        right_layout.addWidget(primary_axis_group)

        secondary_axis_group = QtWidgets.QGroupBox("Secondary Axis")
        secondary_axis_layout = QtWidgets.QHBoxLayout(secondary_axis_group)
        self.secondary_axis_radio_grp = QtWidgets.QButtonGroup()
        self.secondary_axis_radio_x = QtWidgets.QRadioButton("X")
        self.secondary_axis_radio_y = QtWidgets.QRadioButton("Y")
        self.secondary_axis_radio_z = QtWidgets.QRadioButton("Z")
        self.secondary_axis_radio_none = QtWidgets.QRadioButton("None")
        self.secondary_axis_radio_grp.addButton(self.secondary_axis_radio_x)
        self.secondary_axis_radio_grp.addButton(self.secondary_axis_radio_y)
        self.secondary_axis_radio_grp.addButton(self.secondary_axis_radio_z)
        self.secondary_axis_radio_grp.addButton(self.secondary_axis_radio_none)
        secondary_axis_layout.addWidget(self.secondary_axis_radio_x)
        secondary_axis_layout.addWidget(self.secondary_axis_radio_y)
        secondary_axis_layout.addWidget(self.secondary_axis_radio_z)
        secondary_axis_layout.addWidget(self.secondary_axis_radio_none)
        right_layout.addWidget(secondary_axis_group)

        secondary_axis_orient_group = QtWidgets.QGroupBox("Secondary Axis")
        secondary_axis_orient_layout = QtWidgets.QHBoxLayout(secondary_axis_orient_group)
        self.secondary_axis_orient_radio_grp = QtWidgets.QButtonGroup()
        self.secondary_axis_orient_radio_x = QtWidgets.QRadioButton("X")
        self.secondary_axis_orient_radio_y = QtWidgets.QRadioButton("Y")
        self.secondary_axis_orient_radio_z = QtWidgets.QRadioButton("Z")
        self.secondary_axis_orient_radio_grp.addButton(self.secondary_axis_orient_radio_x)
        self.secondary_axis_orient_radio_grp.addButton(self.secondary_axis_orient_radio_y)
        self.secondary_axis_orient_radio_grp.addButton(self.secondary_axis_orient_radio_z)
        secondary_axis_orient_layout.addWidget(self.secondary_axis_orient_radio_x)
        secondary_axis_orient_layout.addWidget(self.secondary_axis_orient_radio_y)
        secondary_axis_orient_layout.addWidget(self.secondary_axis_orient_radio_z)

        direction_comboBox = QtWidgets.QComboBox()
        direction_comboBox.addItems([" + ", " - "])
        secondary_axis_orient_layout.addWidget(direction_comboBox)

        right_layout.addWidget(secondary_axis_orient_group)

        self.orient_children_cb = QtWidgets.QCheckBox("Orient Children")
        right_layout.addWidget(self.orient_children_cb)

        self.reorient_local_scale_cb = QtWidgets.QCheckBox("Reorient Local Scale Axes")
        right_layout.addWidget(self.reorient_local_scale_cb)

        splitter.addWidget(right_widget)
        splitter.addWidget(left_widget)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine) 
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)  

        main_button_layout = QtWidgets.QHBoxLayout(self)

        orient_button = QtWidgets.QPushButton("Orient")
        orient_button.setStyleSheet("background-color: rgb(50, 200, 110); color: white;")
        orient_button.clicked.connect(self.close)
        main_button_layout.addWidget(orient_button)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("background-color: rgb(230, 75, 60); color: white;")
        close_button.clicked.connect(self.close)
        main_button_layout.addWidget(close_button)

        layout.addWidget(splitter)
        layout.addWidget(separator)
        layout.addLayout(main_button_layout)
        

    def load_selection(self):
        # This function adds selected objects to the list
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            self.selection_list.addItem("No selection")
        else:
            self.selection_list.clear()
            for obj in selected_objects:
                self.selection_list.addItem(obj)

    def collect_data(self):
        # This function collects data from the UI elements
        self.selected_items = [self.selection_list.item(i).text() for i in range(self.selection_list.count())]
        self.transform_choice = "translate" if self.translate_rb.isChecked() else "rotate"
        self.axis_selection = [axis for axis, checkbox in {"X": self.x_cb, "Y": self.y_cb, "Z": self.z_cb}.items() if checkbox.isChecked()]

        self.create_dynamic_chain()

    def create_dynamic_chain(self):
        # This function creates the dynamic chain
        chain_elements = self.selected_items
        expression = ""

        if chain_elements:
            if not cmds.attributeQuery('Delay', node=chain_elements[0], exists=True):
                cmds.addAttr(chain_elements[0], longName='Delay', attributeType='double', defaultValue=2.0, keyable=True)

            if not cmds.attributeQuery('Amplitude', node=chain_elements[0], exists=True):
                cmds.addAttr(chain_elements[0], longName='Amplitude', attributeType='double', defaultValue=1.0, keyable=True)

            if not cmds.objExists('inverse_md'):
                inverse_md_node = cmds.createNode('multDoubleLinear', name='inverse_md')
            else:
                inverse_md_node = 'inverse_md'

            if not cmds.isConnected(f"{chain_elements[0]}.Delay", f"{inverse_md_node}.input1"):
                cmds.connectAttr(f"{chain_elements[0]}.Delay", f"{inverse_md_node}.input1")
            cmds.setAttr(f"{inverse_md_node}.input2", -1.0)

        for index, element in enumerate(chain_elements):
            if index != 0:
                delay_md_node_name = f"{element}_delay_md"
                time_ad_node_name = f"{element}_time_ad"

                if not cmds.objExists(delay_md_node_name):
                    delay_md_node = cmds.createNode('multDoubleLinear', name=delay_md_node_name)
                else:
                    delay_md_node = delay_md_node_name

                if not cmds.isConnected(f"{inverse_md_node}.output", f"{delay_md_node}.input1"):
                    cmds.connectAttr(f"{inverse_md_node}.output", f"{delay_md_node}.input1")
                cmds.setAttr(f"{delay_md_node}.input2", index)

                if not cmds.objExists(time_ad_node_name):
                    time_ad_node = cmds.createNode('addDoubleLinear', name=time_ad_node_name)
                else:
                    time_ad_node = time_ad_node_name

                if not cmds.isConnected(f"{delay_md_node}.output", f"{time_ad_node}.input1"):
                    cmds.connectAttr(f"{delay_md_node}.output", f"{time_ad_node}.input1")

                try:
                    cmds.connectAttr("time1.outTime", f"{time_ad_node}.input2")
                except RuntimeError:
                    print('time1.outTime is already connected. IGNORE')

                for axis in self.axis_selection:
                    expression += f"{element}.{self.transform_choice}{axis} = `getAttr - time ({time_ad_node}.output) {chain_elements[0]}.{self.transform_choice}{axis}` * {chain_elements[0]}.Amplitude;\n"
        
        expression_name = 'OrientJoint_EXP'
        if cmds.objExists(expression_name):
            cmds.expression(expression_name, edit=True, string=expression)
        else:
            cmds.expression(name=expression_name, string=expression)

def show_orient_tool_ui():
    # This function shows the UI
    if cmds.window("OrientJoint", exists=True):
        cmds.deleteUI("OrientJoint", wnd=True)

    window = OrientJoint()
    window.show()

show_orient_tool_ui()