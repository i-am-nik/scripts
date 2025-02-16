import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.cmds as cmds

WINDOW_TITLE = "Dynamic Chain UI"
MIN_WIDTH = 300
MIN_HEIGHT = 200

def maya_main_window():
    """Get the main window of Maya."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class DynamicChain(QtWidgets.QDialog):
    """A dialog for creating dynamic chains in Maya."""
    def __init__(self, parent=maya_main_window()):
        """Initialize the DynamicChain dialog."""
        super(DynamicChain, self).__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMinimumHeight(MIN_HEIGHT)

        self.selected_items = []
        self.transform_choice = ""
        self.axis_selection = []

        self.create_ui()

    def create_ui(self):
        """Set up the user interface."""
        layout = QtWidgets.QVBoxLayout(self)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)

        self.note_label = QtWidgets.QLabel("First element is treated as animation source")
        left_layout.addWidget(self.note_label)

        self.selection_list = QtWidgets.QListWidget()
        self.selection_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
        self.load_selection_btn = QtWidgets.QPushButton("Load Selection")
        self.load_selection_btn.setStyleSheet("background-color: #3498db; color: white; font-size: 12px; font-weight: bold;")

        self.load_selection_btn.clicked.connect(self.load_selection)

        left_layout.addWidget(self.selection_list)
        left_layout.addWidget(self.load_selection_btn)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        transforms_group = QtWidgets.QGroupBox("Transforms")
        transforms_group.setStyleSheet("font-weight: bold;")
        transforms_layout = QtWidgets.QVBoxLayout(transforms_group)
        self.translate_rb = QtWidgets.QRadioButton("Translate")
        self.rotate_rb = QtWidgets.QRadioButton("Rotate")
        transforms_layout.addWidget(self.translate_rb)
        transforms_layout.addWidget(self.rotate_rb)
        right_layout.addWidget(transforms_group)

        self.rotate_rb.setChecked(True)  # Set default choice to Rotate

        axis_group = QtWidgets.QGroupBox("Axis")
        axis_group.setStyleSheet("font-weight: bold;")
        axis_layout = QtWidgets.QHBoxLayout(axis_group)
        self.x_cb = QtWidgets.QCheckBox("X")
        self.y_cb = QtWidgets.QCheckBox("Y")
        self.z_cb = QtWidgets.QCheckBox("Z")
        axis_layout.addWidget(self.x_cb)
        axis_layout.addWidget(self.y_cb)
        axis_layout.addWidget(self.z_cb)
        right_layout.addWidget(axis_group)

        self.x_cb.setChecked(True)  # Default to X checked
        self.y_cb.setChecked(True)  # Default to Y checked
        self.z_cb.setChecked(True)  # Default to Z checked

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_btn.setStyleSheet("background-color: #32c86e; color: white; font-size: 12px; font-weight: bold;")
        self.create_btn.clicked.connect(self.collect_data)

        right_layout.addWidget(self.create_btn)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("background-color: #e64b3c; color: white; font-size: 12px;")
        close_button.clicked.connect(self.close)
        
        layout.addWidget(splitter)
        layout.addWidget(close_button)

    def load_selection(self):
        """Add selected objects to the list."""
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            self.selection_list.addItem("No selection")
        else:
            self.selection_list.clear()
            for obj in selected_objects:
                self.selection_list.addItem(obj)

    def collect_data(self):
        """Collect data from the UI elements."""
        self.selected_items = [self.selection_list.item(i).text() for i in range(self.selection_list.count())]
        self.transform_choice = "translate" if self.translate_rb.isChecked() else "rotate"
        self.axis_selection = [axis for axis, checkbox in {"X": self.x_cb, "Y": self.y_cb, "Z": self.z_cb}.items() if checkbox.isChecked()]

        self.create_dynamic_chain()

    def create_dynamic_chain(self):
        """Create the dynamic chain."""
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
        
        expression_name = 'dynamicChain_EXP'
        if cmds.objExists(expression_name):
            cmds.expression(expression_name, edit=True, string=expression)
        else:
            cmds.expression(name=expression_name, string=expression)

def show_dynamic_chain_ui():
    """Show the Dynamic Chain UI."""
    if cmds.window("DynamicChain", exists=True):
        cmds.deleteUI("DynamicChain", wnd=True)

    window = DynamicChain()
    window.show()

show_dynamic_chain_ui()