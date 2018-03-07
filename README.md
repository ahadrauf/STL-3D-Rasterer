# STL-3D-Rasterer
This software is designed to quickly visualize binary STL files for CAD models for easy analysis without needing to open an actual CAD software. It is fundamentally designed as a supplement for CAD tools, allowing users to quickly display the STL structure without waiting for their CAD software to open or needing to overly burden their GPU.

Currently, the software supports dragging, zooming, and rotating the visualization in 3D space. It also facilitates early identification of potential weak points in the design structure through a color gradient based on support density, which helps to predict the security of joints and other key stress points.

The program uses PyOpenGL, a variant of OpenGL, to implement hardware-accelerated graphics rendering and to minimize CPU usage and to take advtange of its optimized culling implementation and cross-platform functionality. Currently, the program begins to experience significant slowdown when trying to display more than about 50,000 - 75,000 triangles (which roughly corresponds to a 3-4 MB binary STL file); the current settings defined by "maxLength" and "simplificationFactor" in gui.py are set to prevent such a situation, but they can also be manually adjusted based on the situation.

Examples of the simulation's appearance for a variety of CAD models can be found in the `/examples` folder.

Dependencies:
 - PyGame 1.3.0 or newer, for the front-end graphics: http://www.pygame.org/news
 - PyOpenGL 3.1.0 or newer: http://pyopengl.sourceforge.net/ (it's possible that older versions of PyOpenGL will work as well, but they're no longer available for download so they haven't been tested yet)
