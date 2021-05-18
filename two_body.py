import numpy as np
from scipy.integrate import odeint

import plotly.graph_objects as go
from plotly.graph_objs import Scatter


class two_body:
    def __init__(self, bodies, time_span, dt=404, G=None, xy=False, animate=True):
        self.xy = xy
        self.animate = animate

        self.G = G
        self.dt = dt
        self.bodies = bodies

        self.body_a = bodies[0]
        self.a_radius = self.body_a['Radius']
        self.a_color = self.body_a['Color']
        self.a_color_gradient = self.body_a['Color_Gradient']

        self.body_b = bodies[1]
        self.b_radius = self.body_b['Radius']
        self.b_color = self.body_b['Color']
        self.b_color_gradient = self.body_b['Color_Gradient']

        self.m_a = self.body_a['Mass']
        self.m_b = self.body_b['Mass']

        self.time_span = np.linspace(0, time_span, dt)

        self.init_params = []

        for body_r in self.bodies:
            self.init_params.append(body_r['init_position'])

        for body_v in self.bodies:
            self.init_params.append(body_v['init_velocity'])

        self.init_params = np.array(self.init_params).flatten()
        print(self.init_params)

    def two_body_ode(self, init_params, time_span, G, m_a, m_b):
        self.r_a = init_params[:2]
        self.r_b = init_params[2:4]
        self.v_a = init_params[4:6]
        self.v_b = init_params[6:8]

        self.r_a_x, self.r_a_y = self.r_a
        self.v_a_x, self.v_a_y = self.v_a

        self.r_b_x, self.r_b_y = self.r_b
        self.v_b_x, self.v_b_y = self.v_b

        self.r = np.linalg.norm(self.r_a - self.r_b)

        # Position | ∫dx/dt
        self.dr_a_dt = self.v_a
        self.dr_b_dt = self.v_b

        # Velocity | ∫dv/dt
        self.dv_a_dt = self.G * \
            ((self.m_b * ((self.r_b - self.r_a) / self.r)) / self.r ** 2)
        self.dv_b_dt = self.G * \
            ((self.m_a * ((self.r_a - self.r_b) / self.r)) / self.r ** 2)

        return np.array([self.dr_a_dt, self.dr_b_dt, self.dv_a_dt, self.dv_b_dt]).flatten()

    def two_body_sol(self):
        self.two_body_sol = odeint(
            self.two_body_ode, self.init_params, self.time_span, args=(self.G, self.m_a, self.m_b))

        return self.two_body_sol

    def plot(self):
        self.two_body_sol = self.two_body_sol()

        self.r_a_sol = self.two_body_sol[:, :2]
        self.r_b_sol = self.two_body_sol[:, 2:4]
        self.v_a_sol = self.two_body_sol[:, 4:6]
        self.v_b_sol = self.two_body_sol[:, 6:8]

        self.r_a_x_sol = np.array(self.r_a_sol[:, :1])
        self.r_a_y_sol = np.array(self.r_a_sol[:, 1:2])
        self.r_b_x_sol = np.array(self.r_b_sol[:, :1])
        self.r_b_y_sol = np.array(self.r_b_sol[:, 1:2])

        self.r_a_x_sol_ = self.r_a_x_sol[:, 0].tolist()
        self.r_a_y_sol_ = self.r_a_y_sol[:, 0].tolist()
        self.r_b_x_sol_ = self.r_b_x_sol[:, 0].tolist()
        self.r_b_y_sol_ = self.r_b_y_sol[:, 0].tolist()

        self.Colors = [
            '#636ef9',
            '#ef553b',
            'tomato',
            'limegreen',
            'crimson',
            'indigo',
            'saddlebrown',
            'deeppink',
            'slategray',
            'gold',
            'navy'
        ]

        self.two_body_plot_objects = []

        self.r_a_trace = go.Scatter(
            x=self.r_a_x_sol_,
            y=self.r_a_y_sol_,
            name='Body A',
            showlegend=False,
            mode='lines',
            line=dict(color=self.Colors[0], width=4)
        )

        self.two_body_plot_objects.append(self.r_a_trace)

        self.r_b_trace = go.Scatter(
            x=self.r_b_x_sol_,
            y=self.r_b_y_sol_,
            name='Body B',
            showlegend=False,
            mode='lines',
            line=dict(color=self.Colors[1], width=4)
        )

        self.two_body_plot_objects.append(self.r_b_trace)

        self.a_ = go.Scatter(x=[self.r_a_x_sol_[-1]], y=[self.r_a_y_sol_[-1]],
                             marker=dict(color=self.Colors[0], size=12,
                                         line=dict(width=2, color='DarkSlateGrey')),
                             name="Body A - Final Position"
                             )

        self.two_body_plot_objects.append(self.a_)

        self.b_ = go.Scatter(x=[self.r_b_x_sol_[-1]], y=[self.r_b_y_sol_[-1]],
                             marker=dict(color=self.Colors[1], size=12,
                                         line=dict(width=2, color='DarkSlateGrey')),
                             name="Body B - Final Position"
                             )

        self.two_body_plot_objects.append(self.b_)

        self.two_body_plot_layout = go.Layout(title='Stable Evolution of a Two-Body System in Two-Dimensional Space',
                                              xaxis=dict(title='x (km)',
                                                         range=[-1, 1.5]),
                                              yaxis=dict(title='y (km)',
                                                         range=[-0.5, 4.75])
                                              )

        self.two_body_plot_xy_static_traj = go.Figure(data=self.two_body_plot_objects,
                                                      layout=self.two_body_plot_layout)
        self.two_body_plot_xy_static_traj.show()

        if self.animate:
            self.r_a_trace = go.Scatter(x=self.r_a_x_sol_[:2],
                                        y=self.r_a_y_sol_[:2],
                                        name='Body A',
                                        showlegend=False,
                                        mode='lines',
                                        line=dict(width=4))

            self.r_b_trace = go.Scatter(x=self.r_b_x_sol_[:2],
                                        y=self.r_b_y_sol_[:2],
                                        name='Body B',
                                        showlegend=False,
                                        mode='lines',
                                        line=dict(width=4))

            self.a_ = go.Scatter(x=self.r_a_x_sol_[:1],
                                 y=self.r_a_y_sol_[:1],
                                 name='Body A',
                                 mode='markers',
                                 marker=dict(color=self.Colors[0], size=12,
                                             line=dict(width=2, color='DarkSlateGrey'))
                                 )

            self.b_ = go.Scatter(x=self.r_b_x_sol_[:1],
                                 y=self.r_b_y_sol_[:1],
                                 name='Body B',
                                 mode='markers',
                                 marker=dict(color=self.Colors[1], size=12,
                                             line=dict(width=2, color='DarkSlateGrey'))
                                 )

            self.two_body_plot_trace_frames = [dict(data=[
                dict(type='scatter',
                     x=self.r_a_x_sol_[: r + 1],
                     y=self.r_a_y_sol_[: r + 1]),
                dict(type='scatter',
                     x=self.r_b_x_sol_[: r + 1],
                     y=self.r_b_y_sol_[: r + 1]),
                dict(type='scatter',
                     x=self.r_a_x_sol_[r - 1: r],
                     y=self.r_a_y_sol_[r - 1: r]),
                dict(type='scatter',
                     x=self.r_b_x_sol_[r: r + 1],
                     y=self.r_b_y_sol_[r: r + 1])],
                traces=[0, 1, 2, 3],
            )for r in range(1, len(self.r_a_x_sol_))]

            self.two_body_plot_layout = go.Layout(title='Stable Evolution of a Two-Body System in Two-Dimensional Space',
                                                  xaxis=dict(title='x (km)',
                                                             range=[-1, 1.5]),
                                                  yaxis=dict(title='y (km)',
                                                             range=[-0.5, 4.75]),
                                                  updatemenus=[dict(type='buttons',
                                                                    buttons=[dict(label='Play',
                                                                                  method='animate',
                                                                                  args=[None, dict(frame=dict(
                                                                                      duration=3, redraw=False))])])]
                                                  )

            self.two_body_plot_xy_animated_traj = go.Figure(data=[self.r_a_trace, self.r_b_trace, self.a_, self.b_],
                                                            frames=self.two_body_plot_trace_frames, layout=self.two_body_plot_layout)
            self.two_body_plot_xy_animated_traj.show()


G = 6.67428e-11  # Universal Gravitaion Constant | N m^2 kg^-2

m_a = 0.1e10  # Mass - Body A | kg
m_b = 0.1e6  # Mass - Body B | kg

r_a = [-0.5, 0]  # Initial Position - Body A | m
r_b = [0.5, 0]  # Initial Position -  Body B | m

v_a = [0.02, 0.1]  # Initial Velocity - Body A | m s^-1
v_b = [-0.08, -0.06]  # Initial Velocity - Body B | m s^-1

a = {'Name': 'a',
     'Mass': m_a,
     'init_position': r_a,
     'init_velocity': v_a,
     'Radius': .125,
     'Color': "dodgerblue",
     'Color_Gradient': "mediumseagreen"
     }

b = {'Name': 'b',
     'Mass': m_b,
     'init_position': r_b,
     'init_velocity': v_b,
     'Radius': .1,
     'Color': "darkred",
     'Color_Gradient': "crimson"
     }

bodies = [a, b]

time_span = 36

classical_two_body = two_body(bodies, time_span, G=G)

classical_two_body.plot()
