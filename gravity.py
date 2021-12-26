import numpy as np
import plotly.graph_objects as go


class acc_field:
    def __init__(self, orbit, n, masking = 3):
        self.bodies = orbit["bodies"]
        self.angular_vel = orbit["angular_vel"]
        self.masking = masking

        self.xlim = self.ylim = 3/2 * max([abs(body["position"]) for body in self.bodies])
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


    def contour(self):
        fig = go.Figure(data = 
                        go.Contour(
                            x=self.x[:,0],
                            y=self.y[0,:],
                            z=np.abs(self.g).T,
                            contours_coloring='lines',
                            contours=dict(
                                start=0,
                                end=np.average(np.abs(self.g))/self.masking)
                            )
                        )
        fig.update_layout(width = 600, height = 600)
        fig.show()


def main():
    angular_vel = 2*np.pi/(28*24*3600)
    bodies = [dict(mu = 3.986004418e14, position = 0, radius = 6.371e6),        # Earth
              dict(mu = 4.9048695e12, position = 384.4e6, radius = 1.7374e6)]   # Moon

    lagrange = acc_field(dict(bodies = bodies, angular_vel = angular_vel), 100, 1.5)
    lagrange.contour()


if __name__ == '__main__':
    main()