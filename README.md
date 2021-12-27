# Gravityfield

Gravityfield calculates the relative acceleration of arbitrary celestial bodies in a 2-dimensional rotating reference frame. **It assumes that relative velocity is 0**. 

With the use of numpy and complex numbers, it does so quickly and efficiently. It also uses plotly to make the visualization of the field easier.

<p align="center">
    <br>
    <img src="https://i.imgur.com/KsIirxp.png" width="400"/>
    <br>
<p>

## Installing

Install with pip:

```python
pip install gravityfield
```

Install from source:

```bash
git clone https://github.com/nesfvillar/gravityfield.git
```

Insert gravityfield.py in your work folder and import as normal.

Requires numpy and plotly.

## An example

```python
import gravityfield as gf

contour_title = 'Absolute value of acceleration near the Earth-Moon system'
angular_vel = 2.9e-6
bodies = [dict(mu = 3.986004418e14, position = 0, radius = 6.371e6),
          dict(mu = 4.9048695e12, position = 384.4e6, radius = 1.7374e6)]

# Calculates the acceleration field
earth_moon = gf.gravityfield(bodies, angular_vel)

# Plots the contour of the acceleration field
earth_moon.contour(title = contour_title)


```

## I want to simulate an orbit

You can use the values calculated from the field, and then **subtract**, from the acceleration in the position of your satellite, the coriolis acceleration. The result is the relative acceleration from which you can progate an orbit.

This has the upside that you calculate most of the terms of the acceleration one time, and then only need to iterate the coriolis effect.

## I have no desire to plot the result, or want to use another library

You can download the source code and remove all parts that use plotly, so as to only calculate the acceleration field, and then do whatever you desire.


