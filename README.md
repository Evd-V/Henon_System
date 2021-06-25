# The Henon Attractor

### Background

*Blabla*

### The Code

This repository contains code regarding the Hénon attractor; it has a number of different files. The `Full_Attractor.py` contains functions that define how the Hénon map is built up. This includes the three different steps that Hénon used in his original paper; starting from an ellipse and subsequently applying the three different transformations that define the map. Furthermore, a function that defines the full map is also defined. I have attempted to optimize the function as much as possible such that a large amount of points can be generated. As of right now it can generate 1 million points in about 7 seconds and 10 million points in a minute or two.

The `lyapunov.py` file contains functions associated with the calculation of the Lyapunov exponents of the Hénon map. As of right now it is not fully optimized and the computation of the exponents is not super accurate but it does give the approximate values. Moreover, the computation time for a relatively small number of Lyapunov exponents is quite long. To deal with this the code has to be further optimized by for example including a part that calculates the exponents for point attractors according to a different program which results in a smaller computation time. For the creation of a larger grid of these exponents a text file will be created to save all exponents to such that they can be reused later. This file also contains function to find the exponents for a range of 'a' and 'b' values and a function that determines the type of attractor based on its Lyapunov exponents.

The `trapping_region.py` file contains functions considering the trapping region of the Hénon attractor. Next to this the image of the trapping region can also be obtained with functions that are defined here. A property of the Hénon map is that the image of the trapping region will remain inside the trapping region itself. However, it is of course possible to find the image of the image; it can be shown that this also remains wihtin the trapping region. One can, in theory, continue this indefinitely; this file contains a function which makes it possible to obtain and plot the *n*th order image of the trapping region. This gives a more visual representation of the property that these always lay within the original trapping region.

### Done and To Do:

A rough list of what has been done and what is left to do:

- :white_check_mark: Added basic functions regarding the Hénon attractor;
- [ ] Add option for 'zooming' in on a specific part on the Hénon map;
- :white_check_mark: Added the trapping region;
- :white_check_mark: Added the image of the trapping region;
- :white_check_mark: Added code to compute Lyapunov exponents;
- [ ] Improve code for the computation of Lyapunov exponents;
- [ ] Add notebook with plots;
- [ ] Add functions to determine whether attractor is a point attractor or a limit cycle, if so what is the period?
- [ ] Find Lyapunov exponents for a point attractor;
- [ ] Add code for creatign a text file to save the generated Lyapunov exponents for later use;
- [ ] More...
