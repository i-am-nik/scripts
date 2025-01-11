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

    def __init__(self, parent=None):
        if JointCreatorUI._instance is not None:
            JointCreatorUI._instance.close()  # Close the existing instance before creating a new one
        super(JointCreatorUI, self).__init__(parent)

        # Set window title and parent
        self.setWindowTitle("Joint On Curve")
        self.setFixedWidth(250)
        self.setFixedHeight(500)
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
        self.title_label = QtWidgets.QLabel("Joint On Curve")
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

        # Curve selection
        self.curve_label = QtWidgets.QLabel("Select Curve:")

        # Text box to display selected curves
        self.curve_textbox = QtWidgets.QLineEdit(self)
        self.curve_textbox.setPlaceholderText("No curve selected")
        self.curve_textbox.setReadOnly(False)

        # Select Curve button
        self.curve_button = QtWidgets.QPushButton("Update Curve Selection")
        self.curve_button.clicked.connect(self.update_curve_selection)

        # Number of joints
        self.num_joints_label = QtWidgets.QLabel("Number of Joints:")
        self.num_joints_spin = QtWidgets.QSpinBox()
        self.num_joints_spin.setValue(5)
        self.num_joints_spin.setMinimum(2)
        self.num_joints_spin.setMaximum(999)

        # Naming pattern split into prefix, name, suffix
        self.naming_label_layout = QtWidgets.QHBoxLayout()

        self.prefix_label = QtWidgets.QLabel("Prefix:")
        self.prefix_input = QtWidgets.QLineEdit("c")
        self.naming_label_layout.addWidget(self.prefix_label)

        self.name_label = QtWidgets.QLabel("  Name:")
        self.name_input = QtWidgets.QLineEdit("spine")
        self.naming_label_layout.addWidget(self.name_label)

        self.suffix_label = QtWidgets.QLabel("    Suffix:")
        self.suffix_input = QtWidgets.QLineEdit("jnt")
        self.naming_label_layout.addWidget(self.suffix_label)

        # Create a horizontal layout for prefix, name, and suffix with underscores in between
        self.name_layout = QtWidgets.QHBoxLayout()
        self.name_layout.addWidget(self.prefix_input)
        self.name_layout.addWidget(QtWidgets.QLabel("_"))  # Underscore between prefix and name
        self.name_layout.addWidget(self.name_input)
        self.name_layout.addWidget(QtWidgets.QLabel("_"))  # Underscore between name and suffix
        self.name_layout.addWidget(self.suffix_input)

        # Example label showing final naming pattern
        self.example_label = QtWidgets.QLabel("Output: c_spine*_jnt")

        # Joint radius
        self.radius_label = QtWidgets.QLabel("Joint Radius:")
        self.radius_input = QtWidgets.QDoubleSpinBox()
        self.radius_input.setValue(1.0)
        self.radius_input.setMinimum(0.01)
        self.radius_input.setSingleStep(0.1)

        # Create joint chain option
        self.create_chain_label = QtWidgets.QLabel("Hiearchy:")
        self.create_chain_layout = QtWidgets.QHBoxLayout()
        self.create_chain_radio_grp = QtWidgets.QButtonGroup()
        self.create_chain_radio1 = QtWidgets.QRadioButton('Joint chain')
        self.create_chain_radio1.setChecked(True)
        self.create_chain_radio2 = QtWidgets.QRadioButton('Standalone joints')
        self.create_chain_layout.addWidget(self.create_chain_radio1)
        self.create_chain_layout.addWidget(self.create_chain_radio2)
        self.create_chain_radio_grp.addButton(self.create_chain_radio1)
        self.create_chain_radio_grp.addButton(self.create_chain_radio2)

        # Orientation type
        self.orient_type_label = QtWidgets.QLabel("Orientation Type:")
        self.orient_type_layout = QtWidgets.QHBoxLayout()
        self.orient_type_radio_grp = QtWidgets.QButtonGroup()
        self.orient_type_radio1 = QtWidgets.QRadioButton('World')
        self.orient_type_radio2 = QtWidgets.QRadioButton('Curve')
        self.orient_type_radio2.setChecked(True)
        self.orient_type_layout.addWidget(self.orient_type_radio1)
        self.orient_type_layout.addWidget(self.orient_type_radio2)
        self.orient_type_radio_grp.addButton(self.orient_type_radio1)
        self.orient_type_radio_grp.addButton(self.orient_type_radio2)
        # Create joints button
        self.create_button = QtWidgets.QPushButton("Create Joints")
        self.create_button.clicked.connect(self.create_joints)

        # Add all UI elements to layout
        self.layout().addWidget(self.hyperlink_label)
        self.layout().addWidget(self.curve_label)
        self.layout().addWidget(self.curve_textbox)
        self.layout().addWidget(self.curve_button)
        self.layout().addWidget(self.num_joints_label)
        self.layout().addWidget(self.num_joints_spin)
        self.layout().addLayout(self.naming_label_layout)  # Add the new horizontal layout
        self.layout().addLayout(self.name_layout)  # Add the new horizontal layout
        self.layout().addWidget(self.example_label)
        self.layout().addWidget(self.radius_label)
        self.layout().addWidget(self.radius_input)
        self.layout().addWidget(self.create_chain_label)
        self.layout().addLayout(self.create_chain_layout)
        self.layout().addWidget(self.orient_type_label)
        self.layout().addLayout(self.orient_type_layout)
        self.layout().addWidget(self.create_button)

        # Apply updated styles
        self.apply_styles()

        # Connect text changes to update the example label
        self.prefix_input.textChanged.connect(self.update_example_label)
        self.name_input.textChanged.connect(self.update_example_label)
        self.suffix_input.textChanged.connect(self.update_example_label)

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

    def update_example_label(self):
        # Get the current text from the prefix, name, and suffix fields
        prefix = self.prefix_input.text()
        name = self.name_input.text()
        suffix = self.suffix_input.text()

        # Ensure there is an underscore between prefix-name and name-suffix
        if prefix and not prefix.endswith('_'):
                prefix += '_'
        else:
            pass
        
        if suffix and not suffix.startswith('_'):
                suffix = '_' + suffix
        else:
            pass

        # Update the example label
        example_text = prefix+name+'*'+suffix
        self.example_label.setText("Output: "+example_text)

    def update_curve_selection(self):
        # Get the selected curves in Maya
        selected_curves = cmds.ls(selection=True, type="transform")
        
        # If curves are selected, update the text box with their names
        if selected_curves:
            self.curve_textbox.setText(", ".join(selected_curves))
            # Change the label based on the number of selected curves
            if len(selected_curves) > 1:
                self.num_joints_label.setText("Number of Joints (on each):")
            else:
                self.num_joints_label.setText("Number of Joints:")
        else:
            self.curve_textbox.setText("No curve selected")
            self.num_joints_label.setText("Number of Joints:")

    def get_joint_name(self,prefix,name,index,suffix,num_joints):
        len_joints = len(str(num_joints))
        name = f"{name}{(index+1):0{len_joints}d}"
        if prefix and suffix:
            result = prefix+'_'+name+'_'+suffix
        elif prefix and not suffix:
            result = prefix+'_'+name+suffix
        elif not prefix and suffix:
            result = prefix+name+'_'+suffix
        else:
            result = prefix+name+suffix
        return result

    def create_joints(self):
        # Get values from UI elements
        sel_curves = self.curve_textbox.text()
        if sel_curves == "No curve selected":
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a curve first.")
            return
        
        # data from UI
        num_joints = self.num_joints_spin.value()
        prefix = self.prefix_input.text()
        name = self.name_input.text()
        suffix = self.suffix_input.text()
        radius = self.radius_input.value()
        create_chain = 0 if self.create_chain_radio1.isChecked() else 1
        orient_type = 0 if self.orient_type_radio1.isChecked() else 1

        curve_list = sel_curves.split(',')
        for curve_index in range(len(curve_list)):
            print(curve_list[curve_index])
            curve_degree = cmds.getAttr(curve_list[curve_index]+'.degree')
            curve_spans = cmds.getAttr(curve_list[curve_index]+'.spans')
            
            curve_cvs = curve_degree+curve_spans
            smooth_cvs = curve_cvs*num_joints

            dup_curve = cmds.rebuildCurve(curve_list[curve_index], ch=True, rpo=False, rt=False, end=True, kr=False, kcp=False, kep=True, kt=False, s=smooth_cvs, d=True, tol=0.01)
            dup_curve_shade_node = cmds.listRelatives(dup_curve[0], shapes=True)

            joint_name = []
            if cmds.ls(sl=True):
                cmds.select(cl=True)

            for i in range(num_joints+1):

                joint_cv = (smooth_cvs/num_joints)*i
                joint_pos = cmds.xform((dup_curve_shade_node[0]+'.controlPoints['+str(int(joint_cv))+']'), q=True, t=True)
                joint_name.append(self.get_joint_name(prefix,name,(i+curve_index+(curve_index*num_joints)),suffix,num_joints))
                joint_create = cmds.joint(n=joint_name[i], rad=radius, p=(joint_pos[0],joint_pos[1],joint_pos[2]))

            cmds.delete(dup_curve)

            if orient_type:
                cmds.joint(joint_name[0], e=True, ch=True, oj='yzx', sao='yup')
                for axis in ['x','y','z']:
                    cmds.setAttr((joint_name[-1]+'.jo'+axis),0.0)

            if create_chain:
                children = cmds.listRelatives(joint_name[0], ad=True, type="joint")
                children.reverse()
                for child in children:
                    cmds.parent(child, world=True)


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