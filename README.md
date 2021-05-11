# Henon Project

Repository that contains code regarding the Hénon attractor; as of right now this contains two files. The Full_Attractor.py contains functions that define how the Hénon map is built up. This includes the three different steps that Hénon used in his original paper; starting from an ellipse and subsequently applying the three different transformations that define the map. Furthermore, a function that defines the full map is also defined. I have attempted to optimize the function as much as possible such that a large amount of points can be generated. As of right now it can generate 1 million points in about 7 seconds and 10 million points in a minute or two. The file lyapunov.py contains functions associated with the calculation of the lyapunov exponents of the Hénon map. As of right now it is not fully optimized and the computation of the exponents is not super accurate but it does give the approximate values.

To Do:

- [ ] Add option for 'zooming' in on a specific part on the Hénon map;
- [ ] Add the trapping region;
- [ ] Add the image of the trapping region;
- [ ] Improve code for the computation of Lyapunov exponents;
- [ ] Add notebook with plots;
- [ ] More...
