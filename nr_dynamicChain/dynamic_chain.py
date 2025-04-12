import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.cmds as cmds

# Constants for window dimensions and title
WINDOW_TITLE = "Dynamic Chain UI"
MIN_WIDTH = 300
MIN_HEIGHT = 200

# Constants for attribute names
DELAY_ATTR = 'Delay'
AMPLITUDE_ATTR = 'Amplitude'


def maya_main_window() -> QtWidgets.QWidget:
    """
    Get the main window of Maya.

    This function retrieves Maya's main window using the Maya OpenMayaUI API 
    and wraps it into a Qt widget for integration with PySide2.

    Returns:
        QWidget: The main window widget of Maya.
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class DynamicChain(QtWidgets.QDialog):
    """
    A dialog window for creating dynamic chains in Maya.

    This dialog enables users to create a dynamic chain of objects, where the 
    transformation (translate or rotate) of one object influences the others. 
    The first selected object is treated as the animation source.

    Attributes:
        selected_items (list): List of the names of selected items.
        transform_choice (str): The chosen transformation type ('translate' or 'rotate').
        axis_selection (list): The list of selected axes (X, Y, Z).
    """

    def __init__(self, parent: QtWidgets.QWidget = maya_main_window()):
        """
        Initialize the DynamicChain dialog.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to Maya's main window.
        """
        super(DynamicChain, self).__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMinimumHeight(MIN_HEIGHT)

        self.selected_items = []  # Stores the names of selected objects
        self.transform_choice = ""  # Stores whether the user selected "translate" or "rotate"
        self.axis_selection = []  # Stores the list of selected axes (e.g., X, Y, Z)

        self.create_ui()

    def create_ui(self):
        """
        Set up the user interface for the DynamicChain dialog.

        This function adds all widgets, layouts, and UI elements necessary for user 
        interaction with the tool. It includes buttons for loading selections, 
        choosing transform types, and selecting axes to apply transformations.
        """
        layout = QtWidgets.QVBoxLayout(self)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Left widget: Contains the selection-related actions and buttons
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

        self.clear_selection_btn = QtWidgets.QPushButton("Clear Selection")
        self.clear_selection_btn.setStyleSheet("background-color: #3498db; color: white; font-size: 12px; font-weight: bold;")
        self.clear_selection_btn.clicked.connect(self.clear_selection)

        left_layout.addWidget(self.clear_selection_btn)

        # Right widget: Contains transform and axis selection options
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        # Transforms selection (translate or rotate)
        transforms_group = QtWidgets.QGroupBox("Transforms")
        transforms_group.setStyleSheet("font-weight: bold;")
        transforms_layout = QtWidgets.QVBoxLayout(transforms_group)
        self.translate_rb = QtWidgets.QRadioButton("Translate")
        self.rotate_rb = QtWidgets.QRadioButton("Rotate")
        transforms_layout.addWidget(self.translate_rb)
        transforms_layout.addWidget(self.rotate_rb)
        right_layout.addWidget(transforms_group)

        self.rotate_rb.setChecked(True)  # Default choice is Rotate

        # Axis selection (X, Y, Z)
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

        # Add the widgets to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("background-color: #e64b3c; color: white; font-size: 12px;")
        close_button.clicked.connect(self.close)

        layout.addWidget(splitter)
        layout.addWidget(close_button)

    def load_selection(self):
        """
        Load selected objects from Maya into the selection list.

        This method updates the UI with the list of currently selected objects in the Maya scene.
        If there are no objects selected, a placeholder message ("No selection") will be added to the list.

        Raises:
            RuntimeError: If there is an error in retrieving or processing the selection.
        """
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            self.selection_list.addItem("No selection")
        else:
            self.selection_list.clear()
            for obj in selected_objects:
                self.selection_list.addItem(obj)

    def collect_data(self):
        """
        Collect the data from the UI and trigger the dynamic chain creation.

        This method checks the user input, verifies that a valid selection exists,
        and gathers the necessary transformation and axis choices. It then calls 
        the method to create the dynamic chain.

        Raises:
            RuntimeError: If no valid selection is made or no axes are selected.
        """
        if self.selection_list.count() == 0 or self.selection_list.item(0).text() == "No selection":
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please load a valid selection before creating the dynamic chain.")
            return

        self.selected_items = [self.selection_list.item(i).text() for i in range(self.selection_list.count())]
        self.transform_choice = "translate" if self.translate_rb.isChecked() else "rotate"
        self.axis_selection = [axis for axis, checkbox in {"X": self.x_cb, "Y": self.y_cb, "Z": self.z_cb}.items() if checkbox.isChecked()]

        # Ensure that at least one axis is selected before proceeding
        if not self.axis_selection:
            QtWidgets.QMessageBox.warning(self, "Axis Selection Error", "Please select at least one axis for transformation.")
            return

        self.create_dynamic_chain()

    def create_or_get_node(self, node_type: str, node_name: str) -> str:
        """
        Create or retrieve a node by name.

        Args:
            node_type (str): The type of the node to create (e.g., 'multDoubleLinear').
            node_name (str): The name of the node to create or find.

        Returns:
            str: The name of the node.
        """
        if not cmds.objExists(node_name):
            return cmds.createNode(node_type, name=node_name)
        return node_name

    def create_dynamic_chain(self):
        """
        Create the dynamic chain by establishing relationships between the selected nodes.

        This function establishes connections between nodes based on the chosen 
        transformation (translate or rotate) and axis selections. The first selected 
        object is used as the "source" for animation, and other objects in the chain 
        follow the transformation.
        """
        chain_elements = self.selected_items
        expression = ""

        if chain_elements:
            prefix = chain_elements[0].replace("|", "_")
            inverse_md_node_name = f'{prefix}_inverse_md'

            self.ensure_attributes_exist(chain_elements[0])

            # Create inverse node for delay and amplitude
            inverse_md_node = self.create_or_get_node('multDoubleLinear', inverse_md_node_name)

            if not cmds.isConnected(f"{chain_elements[0]}.Delay", f"{inverse_md_node}.input1"):
                cmds.connectAttr(f"{chain_elements[0]}.Delay", f"{inverse_md_node}.input1")
            cmds.setAttr(f"{inverse_md_node}.input2", -1.0)

        # Create dynamic chain nodes for each element
        for index, element in enumerate(chain_elements):
            if index != 0:
                delay_md_node_name = f"{prefix}_{element}_delay_md"
                time_ad_node_name = f"{prefix}_{element}_time_ad"

                delay_md_node = self.create_or_get_node('multDoubleLinear', delay_md_node_name)
                if not cmds.isConnected(f"{inverse_md_node}.output", f"{delay_md_node}.input1"):
                    cmds.connectAttr(f"{inverse_md_node}.output", f"{delay_md_node}.input1")
                cmds.setAttr(f"{delay_md_node}.input2", index)

                time_ad_node = self.create_or_get_node('addDoubleLinear', time_ad_node_name)
                if not cmds.isConnected(f"{delay_md_node}.output", f"{time_ad_node}.input1"):
                    cmds.connectAttr(f"{delay_md_node}.output", f"{time_ad_node}.input1")

                if not cmds.isConnected("time1.outTime", f"{time_ad_node}.input2"):
                    cmds.connectAttr("time1.outTime", f"{time_ad_node}.input2")

                for axis in self.axis_selection:
                    expression += f"{element}.{self.transform_choice}{axis} = `getAttr - time ({time_ad_node}.output) {chain_elements[0]}.{self.transform_choice}{axis}` * {chain_elements[0]}.Amplitude;\n"

        expression_name = f'{prefix}_dynamicChain_EXP'
        if cmds.objExists(expression_name):
            cmds.expression(expression_name, edit=True, string=expression)
        else:
            cmds.expression(name=expression_name, string=expression)

    def ensure_attributes_exist(self, node_name: str):
        """
        Ensures that the Delay and Amplitude attributes exist for the first element.

        Args:
            node_name (str): The name of the node to check and add attributes if needed.
        """
        if not cmds.attributeQuery(DELAY_ATTR, node=node_name, exists=True):
            cmds.addAttr(node_name, longName=DELAY_ATTR, attributeType='double', defaultValue=2.0, keyable=True)

        if not cmds.attributeQuery(AMPLITUDE_ATTR, node=node_name, exists=True):
            cmds.addAttr(node_name, longName=AMPLITUDE_ATTR, attributeType='double', defaultValue=1.0, keyable=True)

    def clear_selection(self):
        """
        Clear the current selection list and reset the internal selected items.

        This function resets the selection list UI and clears the selected objects 
        stored in the internal list, allowing the user to start fresh.
        """
        self.selection_list.clear()
        self.selected_items = []


def show_dynamic_chain_ui():
    """
    Display the Dynamic Chain UI dialog.

    This function checks if the DynamicChain window already exists. If so, it 
    deletes the existing window and then creates a new instance of the UI. 
    This ensures that only one instance of the dialog is open at a time.
    """
    if cmds.window("DynamicChain", exists=True):
        cmds.deleteUI("DynamicChain", wnd=True)

    window = DynamicChain()
    window.show()

# Show the UI
show_dynamic_chain_ui()