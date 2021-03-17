import numpy as np
from matplotlib.pyplot import figure, show, savefig

# Creating the parameter values for the ellipse
A_rand = 1.5
B_rand = 0.8

# Creating values
Vals = np.linspace(0, 360, 400)

# Creating the x and y values for the ellipse
Xvals = A_rand * np.cos(np.radians(Vals))
Yvals = B_rand * np.sin(np.radians(Vals))

# A value for a
a = 1.4

# Creating the x and y values for the second step of the transformation
Xtran2 = b * Xtran1
Ytran2 = Ytran1

# ----------------- #
# Step 2
b = 0.3

# Creating the x and y values for the first step of the transformation
Xtran1 = Xvals
Ytran1 = Yvals + 1 - a * Xvals**2

# ----------------- #
# Step 3

# Creating the x and y values for the third step of the transformation
Xtran3 = Ytran2
Ytran3 = Xtran2

# ----------------- #
# Plotting
fig = figure(figsize=(12, 12))
frame = fig.add_subplot(2,2,1)
frame2 = fig.add_subplot(2,2,2)
frame3 = fig.add_subplot(2,2,3)
frame4 = fig.add_subplot(2,2,4)

frame.plot(Xvals, Yvals, color='seagreen', lw=2.4)
frame2.plot(Xtran1, Ytran1, color='teal', lw=2.4)
frame3.plot(Xtran2, Ytran2, color='darkblue', lw=2.4)
frame4.plot(Xtran3, Ytran3, color='seagreen', lw=2.4)

frame.set_xlabel('x')
frame.set_ylabel('y')
frame.set_xlim(-1.6, 1.6)
frame.set_ylim(-2.3, 2)

frame2.set_title('Hénon attractor step 1')
frame2.set_xlabel('x')
frame2.set_ylabel('y')
frame2.set_xlim(-1.6, 1.6)
frame2.set_ylim(-2.3, 2)

frame3.set_title('Hénon attractor step 2')
frame3.set_xlabel('x')
frame3.set_ylabel('y')
frame3.set_xlim(-1.6, 1.6)
frame3.set_ylim(-2.3, 2)

frame4.set_title('Hénon attractor step 3')
frame4.set_xlabel('x')
frame4.set_ylabel('y')
frame4.set_xlim(-1.6, 1.6)
frame4.set_ylim(-2.3, 2)

frame.grid()
frame2.grid()
frame3.grid()
frame4.grid()

fig.tight_layout()

# Uncomment to save the figure
#fig.savefig('Hénon_steps.pdf')

show()
