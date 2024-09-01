# Trigonometric Node Plugin for Maya

This plugin provides a set of custom nodes for Maya, implementing trigonometric functions using polynomial approximation methods. Instead of relying on Taylor series expansions, which can become computationally intensive and less accurate for large angles, this implementation uses Chebyshev polynomials to approximate sine, cosine, tangent, cotangent, secant, and cosecant functions.

## Why Polynomial Approximation?

Polynomial approximations, particularly Chebyshev polynomials, are used in this implementation due to their superior performance in terms of both accuracy and computational efficiency. Chebyshev polynomials are well-suited for approximating functions within a bounded interval and are known for their minimal error margins and faster convergence compared to Taylor series, especially over large domains.

## Memory and Time Complexity

The polynomial approximation method is designed to be efficient in terms of both memory and computational time. The memory footprint is minimal as it only requires storing a small number of polynomial coefficients. The time complexity is O(1) for evaluating each trigonometric function, making it highly suitable for real-time applications.

## Real-Time Usage in 3D and Graphics Design

In the realm of 3D and graphics design, real-time performance is crucial. The nodes provided by this plugin leverage the efficiency of polynomial approximations to deliver rapid and accurate trigonometric computations. This is particularly beneficial in scenarios requiring frequent recalculations of trigonometric values, such as animation and simulation tasks, where high-speed processing is essential.

## Error Rate and Precision

The approximation error for these polynomial methods is less than 0.0002%, ensuring that the results are highly accurate for practical applications. This low error rate contributes to the reliability of the plugin in professional 3D and graphics environments, where precision is paramount.

## Features and Benefits

- **High Performance**: Efficient evaluation of trigonometric functions with O(1) time complexity.
- **Minimal Memory Usage**: Only a few coefficients are needed, reducing the memory footprint.
- **Real-Time Capability**: Optimized for use in interactive and real-time 3D applications.
- **High Accuracy**: Error rate of less than 0.0002% for reliable results.

This plugin is a valuable tool for 3D artists and developers seeking to integrate fast and accurate trigonometric computations into their Maya workflows.

## Installation

1. **Prepare the Plugin Files**

   - Ensure the plugin script file (`trigonometricNodes.py`) is available.

2. **Copy the Plugin Files**

   - Copy `trigonometricNodes.py` to Maya’s script directory or any directory of your choice. Typical paths are:
     - **Windows**:
       ```
       C:\Users\<YourUsername>\Documents\maya\scripts\
       ```
     - **macOS**:
       ```
       /Users/<YourUsername>/Library/Preferences/Autodesk/maya/scripts/
       ```
     - **Linux**:
       ```
       /home/<YourUsername>/maya/scripts/
       ```

3. **Load the Plugin in Maya**

   - **Open Maya**: Launch Maya on your system.

   - **Open the Plugin Manager**:
     - Navigate to `Windows` > `Settings/Preferences` > `Plugin Manager`.

   - **Add the Plugin Path** (if not in the default script directory):
     - Open the Script Editor (`Windows` > `General Editors` > `Script Editor`).
     - Add the plugin directory to Maya’s script paths:
       ```python
       import maya.cmds as cmds
       cmds.evalDeferred('cmds.sysFile("C:/Users/<YourUsername>/Documents/maya/scripts/", addToSearchPath=True)')
       ```

   - **Load the Plugin**:
     - In the Plugin Manager, click the “Browse” button.
     - Locate and select `trigonometricNodes.py`.
     - Check the checkbox next to the plugin’s name to load it.
     - Optionally, check “Auto load” to load the plugin automatically each time Maya starts.

4. **Verify the Plugin**

   - Open the Script Editor in Maya.
   - Run the following commands to check if the nodes are available:
     ```python
     import maya.cmds as cmds
     print(cmds.nodeType("sinNode"))
     print(cmds.nodeType("cosNode"))
     ```
   - You should see the node types listed if the plugin is correctly loaded.

## Usage

After successfully installing the Trigonometric Node Plugin, you can use the custom trigonometric nodes in Autodesk Maya. Follow these instructions to create and use these nodes:

## Creating and Using Trigonometric Nodes

1. **Open Maya**

   - Launch Autodesk Maya on your system.

2. **Access the Node Editor**

   - Navigate to `Windows` > `Node Editor` or `Windows` > `Hypergraph` > `Hypergraph Connections`.

3. **Create a Trigonometric Node**

   - **Add a Node**:
     - In the Node Editor or Hypershade, click the TAB key.
     - Type the name of the node you want to create (e.g., `sinNode`, `cosNode`, `tanNode`, `cotNode`, `secNode`, `cscNode`).

4. **Node Descriptions**

   - **`sinNode`**: Computes the sine of the input angle in degrees.
   - **`cosNode`**: Computes the cosine of the input angle in degrees.
   - **`tanNode`**: Computes the tangent of the input angle in degrees.
   - **`cotNode`**: Computes the cotangent of the input angle in degrees.
   - **`secNode`**: Computes the secant of the input angle in degrees.
   - **`cscNode`**: Computes the cosecant of the input angle in degrees.
## License
### Educational Use Only

This code is free to use for educational purposes, including personal learning and academic projects. However, it cannot be used for commercial purposes or any projects intended for commercial gain.

#### Key Points:
- **Allowed**: Use, modify, and share the code for educational purposes.
- **Not Allowed**: Use the code for commercial projects or gain.

Please provide proper attribution when using or distributing the code. For commercial use, contact the author for licensing options.

**Disclaimer**: This code is provided as-is, with no warranties.

## Contact

For any questions or licensing inquiries, you can reach out to me at:

- **Email**: [nikhilr.fbx@gmail.com](mailto:nikhilr.fbx@gmail.com)
- **LinkedIn**: [Nikhil Ramchandani](https://www.linkedin.com/in/nikrigs/)

Feel free to connect with me for further information or collaboration opportunities.