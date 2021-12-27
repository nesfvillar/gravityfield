import numpy as np
import plotly.graph_objects as go


class acc_field:
    """ Calculate the acceleration field in 2-dimensional space in a rotating reference frame with no relative velocity.

        All calculations are made under the assumption that the same measurement system is used. 
        (i.e. you should not put the mu of the bodies in m^3/s^2 and then the position in km and angular velocity in rad/day, for example. The same goes if you use the imperial system)
        
        !! If you want to calculate the acceleration at any point with relative velocity, 
        SUBTRACT from the corresponding value (the position the object is) in acc_field.g  the coriolis acceleration (in complex form) !!


        Parameters: 

        bodies - List of dicts with information about all the bodies, for example:
            [dict(mu = 3.986004418e14, position = 0, radius = 6.371e6),
             dict(mu = 4.9048695e12, position = 384.4e6, radius = 1.7374e6)]
            
            mu - The gravitational parameter for the body

            position - The position of the body. It is a complex value, so it can be either in cartesian or polar form

            radius - The radius of the body, used to change the value of the internal gravity.
            
             
        angular_vel - Angular velocity of the reference frame.
        
        (optional) lim - This parameter changes the maximum distance from 0 to calculate.
        If it is 1, then it will calculate only to the furthest body, and no more. It is by default 1.5

        (optional) n - Number of points to calculate in a single axis.
        The total number of points calculated will be n**2. It is by default 500
        

        Useful values and functions: 

        acc_field.z - 2-dimensional array of the positions used in acc_field.g.

        acc_field.g - the calculated acceleration field in a 2-dimensional array of complex numbers.
        The real value is the acceleration in the x axis, the imaginary component is the acceleration in the y axis.

        acc_field.contour() - using plotly, draw the contour of the absolute value of the acceleration field.
        
        acc_field.surface() - using plotly, draw the surface plot of the absolute value of the acceleration field. (WIP)"""

        
    def __init__(self, bodies, angular_vel, lim = 3/2,  n = 500):
        self.bodies = bodies
        self.angular_vel = angular_vel

        self.xlim = self.ylim = lim * max([abs(body["position"]) for body in self.bodies])
        self.n = n
        self.x, self.y = np.mgrid[-self.xlim:self.xlim:1j*n, -self.ylim:self.ylim:1j*n]
        self.z = self.x + 1j*self.y

        self.g = self.acceleration_relative(self.bodies, self.angular_vel, self.z)


    def acceleration_gravity(self, body, position):
        return ( 
            # if the position is inside the body
                (np.abs(position - body["position"]) < body["radius"]) *         
                (- body["mu"] / body["radius"]**3 * (position - body["position"])) +
            # else if the position is outside the body
                (np.abs(position - body["position"]) >= body["radius"]) *
                (- body["mu"] / (np.conj(position - body["position"]) * np.abs(position - body["position"])))
        )
                

    def acceleration_transport(self, angular_vel, position):
        return - angular_vel**2 * position


    def acceleration_relative(self, bodies, angular_vel, position):
        acc_rel = - self.acceleration_transport(angular_vel, position)
        for body in bodies:
            acc_rel += self.acceleration_gravity(body, position)
        return acc_rel


    def contour(self, title = '', lines = False, masking = 2):
        """ Draw a contour plot of the absolute value of the acceleration. 
        
        Parameters:

        title - Title for the plot. Default is ''
        
        (optional) lines - Bool value, True if you want a contour with lines instead of filled. 
        Default is False
        
        (optional) masking - Number that changes the maximum value to show in the plot, based on the average. Lower means higher maximum value. 
        Default is 2"""


        fig = go.Figure(data = 
            go.Contour(
                x=self.x[:,0],
                y=self.y[0,:],
                z=np.abs(self.g).T,
                contours_coloring = 'lines' if lines else 'fill',
                contours=dict(
                    start=0,
                    end=np.average(np.abs(self.g))/masking)
            )
        )

        fig.update_layout(title = title, width = 600, height = 600)
        fig.show()


    # TODO add maximum value to surface plot
    def surface(self, title = ''):
        """ Draw a surface plot with the absolute value of the acceleration in the z axis.
        
        At this moment, it has no way of selecting a maximum value to plot, so the contour plot is preferred. 
        
        Parameters: 
        title - Title for the plot. Default is '' """


        fig = go.Figure(data =
            go.Surface(
                x=self.x[:,0],
                y=self.y[0,:],
                z=np.abs(self.g).T
            )
        )

        fig.update_layout(title = title, width = 600, height = 600)
        fig.show()


def main():
    # Earth-Moon example:
    contour_title = 'Absolute value of acceleration near the Earth-Moon system'
    angular_vel = 2*np.pi/(28*24*3600)
    bodies = [dict(mu = 3.986004418e14, position = 0, radius = 6.371e6),
              dict(mu = 4.9048695e12, position = 384.4e6, radius = 1.7374e6)]

    earth_moon = acc_field(bodies, angular_vel)
    earth_moon.contour(title = contour_title)


if __name__ == '__main__':
    main()