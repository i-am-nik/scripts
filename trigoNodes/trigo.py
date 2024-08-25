''' TODO:
    - Make test cases for pure maths functions and find error rate in in approx values
    - Test this code in different conditions in maya
    - Make user manual and report of what it is exactly doing
'''

import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx

def adjust_phase(ang_in_deg):
    """
    Normalize an angle in degrees to the range [-180, 180].

    Parameters:
    ang_in_deg (float): The angle in degrees to be normalized.

    Returns:
    float: The normalized angle in the range [-180, 180] degrees.
    """
    # Normalize the angle to the range [0, 360) degrees
    normalized_ang_in_deg = ang_in_deg % 360
    
    # Adjust to the range [-180, 180] degrees
    if normalized_ang_in_deg > 180:
        return normalized_ang_in_deg - 360
    elif normalized_ang_in_deg < -180:
        return normalized_ang_in_deg + 360
    else:
        return normalized_ang_in_deg

def chev_poly(x):
    """
    Evaluate the Chebyshev polynomial of the first kind of degree 5.

    Parameters:
    x (float): The input value for the Chebyshev polynomial.

    Returns:
    float: The evaluated Chebyshev polynomial value.
    """
    # Coefficients for the Chebyshev polynomial of degree 5
    C0 = 1.276278962
    C1 = -0.285261569
    C2 = 0.009118016
    C3 = -0.000136587
    C4 = 0.000001185
    C5 = -0.000000007

    # Calculate Chebyshev polynomial terms
    T0 = 1
    T1 = x
    T2 = (2 * x ** 2 - 1)
    T3 = (4 * x ** 3 - 3 * x)
    T4 = (8 * x ** 4 - 8 * x ** 2 + 1)
    T5 = (16 * x ** 5 - 20 * x ** 3 + 5 * x)

    # Evaluate the polynomial using the coefficients
    return float(C0 * T0 + C1 * T1 + C2 * T2 + C3 * T3 + C4 * T4 + C5 * T5)

def approximate_sin(ang_in_deg):
    """
    Compute the sine of an angle given in degrees using Chebyshev polynomial approximation.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the sine.

    Returns:
    float: The sine of the angle, rounded to six decimal places.
    """
    # Normalize the angle
    value = adjust_phase(ang_in_deg)
    
    # Convert angle to range [-1, 1] for polynomial evaluation
    x = value / 360
    
    # Compute intermediate values for Chebyshev polynomial
    w = 4 * x
    z = 2 * w * w - 1
    
    # Compute the sine value using the Chebyshev polynomial
    result = chev_poly(z) * w
    
    # Round the result to six decimal places
    return float(round(result, 6))

def approximate_cos(ang_in_deg):
    """
    Compute the cosine of an angle given in degrees based on its sine value.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the cosine.

    Returns:
    float: The cosine of the angle, rounded to six decimal places.
    """
    # Determine the sign of the cosine based on the quadrant
    quad_sign = 1
    if (90 <= ang_in_deg <= 270) or (-270 <= ang_in_deg <= -90):
        quad_sign = -1
    
    # Calculate the cosine value from the relation cos(x)^2 + sin(x)^2 = 1
    result = (1 - approximate_sin(ang_in_deg) ** 2) ** 0.5
    
    # Return the result with the appropriate sign and rounded to six decimal places
    return float(round(quad_sign * result, 6))

def approximate_tan(ang_in_deg):
    """
    Compute the tangent of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the tangent.

    Returns:
    float: The tangent of the angle, rounded to six decimal places, or 'UNDEFINED' if the cosine of the angle is zero.
    """
    # Compute cosine and check for undefined tangent
    cos_val = approximate_cos(ang_in_deg)
    if cos_val == 0:
        return float('inf')  # Represents undefined tangent
    
    # Compute the tangent value tan(x)=sin(x)/cos(x) and round to six decimal places
    return float(round(approximate_sin(ang_in_deg) / cos_val, 6))

def approximate_cot(ang_in_deg):
    """
    Compute the cotangent of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the cotangent.

    Returns:
    float: The cotangent of the angle, rounded to six decimal places, or 'UNDEFINED' if the tangent of the angle is zero or undefined.
    """
    # Compute tangent and check for undefined cotangent
    tan_val = approximate_tan(ang_in_deg)
    if tan_val == float('inf') or tan_val == 0:
        return float('inf')  # Represents undefined cotangent
    
    # Compute the cotangent value cot(x)=1/tan(x) and round to six decimal places
    return float(round(1 / tan_val, 6))
    
def approximate_sec(ang_in_deg):
    """
    Compute the secant of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the secant.

    Returns:
    float: The secant of the angle, rounded to six decimal places, or 'UNDEFINED' if the cosine of the angle is zero.
    """
    # Compute cosine and check for undefined secant
    cos_val = approximate_cos(ang_in_deg)
    if cos_val == 0:
        return float('inf')  # Represents undefined secant
    
    # Compute the secant value sec(x)=1/cos(x) and round to six decimal places
    return float(round(1 / cos_val, 6))

def approximate_csc(ang_in_deg):
    """
    Compute the cosecant of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the cosecant.

    Returns:
    float: The cosecant of the angle, rounded to six decimal places, or 'UNDEFINED' if the sine of the angle is zero.
    """
    # Compute sine and check for undefined cosecant
    sin_val = approximate_sin(ang_in_deg)
    if sin_val == 0:
        return float('inf')  # Represents undefined cosecant
    
    # Compute the cosecant value csc(x)=1/sin(x) and round to six decimal places
    return float(round(1 / sin_val, 6))

# Base class for trigonometric nodes
class BaseTrigoNode(ommpx.MPxNode):
    """
    Base class for trigonometric nodes that handles the common attributes and functionality.

    Attributes:
    inputAttr (MObject): The input attribute for the angle in degrees.
    outputAttr (MObject): The output attribute for the computed trigonometric function.
    """
    inputAttr = om.MObject()
    outputAttr = om.MObject()

    def __init__(self):
        """
        Initialize the BaseTrigoNode by calling the parent constructor.
        """
        super(BaseTrigoNode, self).__init__()

    @staticmethod
    def initialize():
        """
        Initialize the node's attributes: input angle and output result.
        """
        numericAttr = om.MFnNumericAttribute()
        BaseTrigoNode.inputAttr = numericAttr.create("input", "in", om.MFnNumericData.kFloat, 0.0)
        numericAttr.setWritable(True)
        numericAttr.setStorable(True)

        BaseTrigoNode.outputAttr = numericAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
        numericAttr.setWritable(False)
        numericAttr.setStorable(False)

        BaseTrigoNode.addAttribute(BaseTrigoNode.inputAttr)
        BaseTrigoNode.addAttribute(BaseTrigoNode.outputAttr)
        BaseTrigoNode.attributeAffects(BaseTrigoNode.inputAttr, BaseTrigoNode.outputAttr)

# Custom nodes for each trigonometric function
class SinNode(BaseTrigoNode):
    """
    Custom node to compute the sine of an angle.

    Attributes:
    kNodeName (node name): Unique name for the node.
    """
    kNodeName = "sinNode"

    def compute(self, plug, dataBlock):
        """
        Compute the sine of the input angle and output the result.

        Parameters:
        plug (MPlug): The plug that is being evaluated.
        dataBlock (MDataBlock): The data block containing the input/output data handles.
        """
        if plug == SinNode.outputAttr:
            inputValue = dataBlock.inputValue(SinNode.inputAttr).asFloat()
            result = approximate_sin(inputValue)
            outputHandle = dataBlock.outputValue(SinNode.outputAttr)
            outputHandle.setFloat(result)
            outputHandle.setClean()
        else:
            return om.kUnknownParameter

class CosNode(BaseTrigoNode):
    """
    Custom node to compute the cosine of an angle.

    Attributes:
    kNodeName (node name): Unique name for the node.
    """
    kNodeName = "cosNode"

    def compute(self, plug, dataBlock):
        """
        Compute the cosine of the input angle and output the result.

        Parameters:
        plug (MPlug): The plug that is being evaluated.
        dataBlock (MDataBlock): The data block containing the input/output data handles.
        """
        if plug == CosNode.outputAttr:
            # Get the input angle value
            inputValue = dataBlock.inputValue(CosNode.inputAttr).asFloat()
            # Calculate the cosine of the input angle
            result = approximate_cos(inputValue)
            # Set the output value to the calculated cosine
            outputHandle = dataBlock.outputValue(CosNode.outputAttr)
            outputHandle.setFloat(result)
            # Mark the output handle as clean
            outputHandle.setClean()
        else:
            return om.kUnknownParameter

class TanNode(BaseTrigoNode):
    """
    Custom node to compute the tangent of an angle.

    Attributes:
    kNodeName (node name): Unique name for the node.
    """
    kNodeName = "tanNode"

    def compute(self, plug, dataBlock):
        """
        Compute the tangent of the input angle and output the result.

        Parameters:
        plug (MPlug): The plug that is being evaluated.
        dataBlock (MDataBlock): The data block containing the input/output data handles.
        """
        if plug == TanNode.outputAttr:
            # Get the input angle value
            inputValue = dataBlock.inputValue(TanNode.inputAttr).asFloat()
            # Calculate the tangent of the input angle
            result = approximate_tan(inputValue)
            # Set the output value to the calculated tangent
            outputHandle = dataBlock.outputValue(TanNode.outputAttr)
            outputHandle.setFloat(result)
            # Mark the output handle as clean
            outputHandle.setClean()
        else:
            return om.kUnknownParameter

class CotNode(BaseTrigoNode):
    """
    Custom node to compute the cotangent of an angle.

    Attributes:
    kNodeName (node name): Unique name for the node.
    """
    kNodeName = "cotNode"

    def compute(self, plug, dataBlock):
        """
        Compute the cotangent of the input angle and output the result.

        Parameters:
        plug (MPlug): The plug that is being evaluated.
        dataBlock (MDataBlock): The data block containing the input/output data handles.
        """
        if plug == CotNode.outputAttr:
            # Get the input angle value
            inputValue = dataBlock.inputValue(CotNode.inputAttr).asFloat()
            # Calculate the cotangent of the input angle
            result = approximate_cot(inputValue)
            # Set the output value to the calculated cotangent
            outputHandle = dataBlock.outputValue(CotNode.outputAttr)
            outputHandle.setFloat(result)
            # Mark the output handle as clean
            outputHandle.setClean()
        else:
            return om.kUnknownParameter

class SecNode(BaseTrigoNode):
    """
    Custom node to compute the secant of an angle.

    Attributes:
    kNodeName (node name): Unique name for the node.
    """
    kNodeName = "secNode"

    def compute(self, plug, dataBlock):
        """
        Compute the secant of the input angle and output the result.

        Parameters:
        plug (MPlug): The plug that is being evaluated.
        dataBlock (MDataBlock): The data block containing the input/output data handles.
        """
        if plug == SecNode.outputAttr:
            # Get the input angle value
            inputValue = dataBlock.inputValue(SecNode.inputAttr).asFloat()
            # Calculate the secant of the input angle
            result = approximate_sec(inputValue)
            # Set the output value to the calculated secant
            outputHandle = dataBlock.outputValue(SecNode.outputAttr)
            outputHandle.setFloat(result)
            # Mark the output handle as clean
            outputHandle.setClean()
        else:
            return om.kUnknownParameter

class CscNode(BaseTrigoNode):
    """
    Custom node to compute the cosecant of an angle.

    Attributes:
    kNodeName (node name): Unique name for the node.
    """
    kNodeName = "cscNode"

    def compute(self, plug, dataBlock):
        """
        Compute the cosecant of the input angle and output the result.

        Parameters:
        plug (MPlug): The plug that is being evaluated.
        dataBlock (MDataBlock): The data block containing the input/output data handles.
        """
        if plug == CscNode.outputAttr:
            # Get the input angle value
            inputValue = dataBlock.inputValue(CscNode.inputAttr).asFloat()
            # Calculate the cosecant of the input angle
            result = approximate_csc(inputValue)
            # Set the output value to the calculated cosecant
            outputHandle = dataBlock.outputValue(CscNode.outputAttr)
            outputHandle.setFloat(result)
            # Mark the output handle as clean
            outputHandle.setClean()
        else:
            return om.kUnknownParameter

# Plugin initialization and uninitialization functions

def maya_useNewAPI():
    """
    Indicates that the plugin uses Maya's Python API 2.0.
    """
    pass

def initializePlugin(mobject):
    """
    Initialize the plugin by registering each custom node.

    Parameters:
    mobject (MObject): The MObject representing the plugin.
    """
    mplugin = ommpx.MFnPlugin(mobject, "Your Name", "1.0", "Any")

    try:
        # Register each node with a unique ID
        SinNode.kNodeId = om.MTypeId.nextId()
        mplugin.registerNode(SinNode.kNodeName, SinNode.kNodeId, SinNode.creator, SinNode.initialize, ommpx.MPxNode.kDependNode)
        
        CosNode.kNodeId = om.MTypeId.nextId()
        mplugin.registerNode(CosNode.kNodeName, CosNode.kNodeId, CosNode.creator, CosNode.initialize, ommpx.MPxNode.kDependNode)
        
        TanNode.kNodeId = om.MTypeId.nextId()
        mplugin.registerNode(TanNode.kNodeName, TanNode.kNodeId, TanNode.creator, TanNode.initialize, ommpx.MPxNode.kDependNode)
        
        CotNode.kNodeId = om.MTypeId.nextId()
        mplugin.registerNode(CotNode.kNodeName, CotNode.kNodeId, CotNode.creator, CotNode.initialize, ommpx.MPxNode.kDependNode)
        
        SecNode.kNodeId = om.MTypeId.nextId()
        mplugin.registerNode(SecNode.kNodeName, SecNode.kNodeId, SecNode.creator, SecNode.initialize, ommpx.MPxNode.kDependNode)
        
        CscNode.kNodeId = om.MTypeId.nextId()
        mplugin.registerNode(CscNode.kNodeName, CscNode.kNodeId, CscNode.creator, CscNode.initialize, ommpx.MPxNode.kDependNode)
    except RuntimeError as e:
        om.MGlobal.displayError("Failed to register nodes")

def uninitializePlugin(mobject):
    """
    Uninitialize the plugin by deregistering each custom node.

    Parameters:
    mobject (MObject): The MObject representing the plugin.
    """
    mplugin = ommpx.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode(SinNode.kNodeId)
        mplugin.deregisterNode(CosNode.kNodeId)
        mplugin.deregisterNode(TanNode.kNodeId)
        mplugin.deregisterNode(CotNode.kNodeId)
        mplugin.deregisterNode(SecNode.kNodeId)
        mplugin.deregisterNode(CscNode.kNodeId)
    except RuntimeError as e:
        om.MGlobal.displayError("Failed to deregister nodes")