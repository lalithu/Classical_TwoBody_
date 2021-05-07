import numpy as np
from scipy.integrate import odeint

import plotly.graph_objects as go
from plotly.graph_objs import Scatter

'''
import chart_studio
import chart_studio.plotly as py

username = 'lalithuriti'
api_key = 'WkltoYNWP7gEy8eWuRUI'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
'''

G = 6.67428e-11  # Universal Gravitaion Constant | N m^2 kg^-2

m_a = 0.1e10  # Mass - Body A | kg
m_b = 0.1e6  # Mass - Body B | kg

r_a = [-0.5, 0]  # Initial Position - Body A | m
r_b = [0.5, 0]  # Initial Position -  Body B | m

v_a = [0.02, 0.1]  # Initial Velocity - Body A | m s^-1
v_b = [-0.08, -0.06]  # Initial Velocity - Body B | m s^-1


def two_body(init_params, t, G, m1, m2):
    r_a = init_params[:2]
    r_b = init_params[2:4]
    v_a = init_params[4:6]
    v_b = init_params[6:8]

    r_a_x, r_a_y = r_a
    v_a_x, v_a_y = v_a

    r_b_x, r_b_y = r_b
    v_b_x, v_b_y = v_b

    r = np.linalg.norm(r_a - r_b)

    # Position | ∫dx/dt
    dr_a_dt = v_a
    dr_b_dt = v_b

    # Velocity | ∫dv/dt
    dv_a_dt = G * m_b * ((r_b - r_a) / r) / r ** 2
    dv_b_dt = G * m_a * ((r_a - r_b) / r) / r ** 2

    return np.array([dr_a_dt, dr_b_dt, dv_a_dt, dv_b_dt]).flatten()


init_params = np.array([r_a, r_b, v_a, v_b]).flatten()
print(init_params)

time_span = np.linspace(0, 36, 404)

two_body_sol = odeint(
    two_body, init_params, time_span, args=(G, m_a, m_b))

# print(two_body_sol)

r_a_sol = two_body_sol[:, :2]
r_b_sol = two_body_sol[:, 2:4]
v_a_sol = two_body_sol[:, 4:6]
v_b_sol = two_body_sol[:, 6:8]

r_a_x_sol = np.array(r_a_sol[:, :1])
r_a_y_sol = np.array(r_a_sol[:, 1:2])
r_b_x_sol = np.array(r_b_sol[:, :1])
r_b_y_sol = np.array(r_b_sol[:, 1:2])

r_a_x_sol_ = r_a_x_sol[:, 0].tolist()
r_a_y_sol_ = r_a_y_sol[:, 0].tolist()
r_b_x_sol_ = r_b_x_sol[:, 0].tolist()
r_b_y_sol_ = r_b_y_sol[:, 0].tolist()


# Static Trajectory
two_body_plot_objects = []

r_a_trace = go.Scatter(
    x=r_a_x_sol_,
    y=r_a_y_sol_,
    name='Body A',
    mode='lines',
    line=dict(width=4)
)

two_body_plot_objects.append(r_a_trace)

r_b_trace = go.Scatter(
    x=r_b_x_sol_,
    y=r_b_y_sol_,
    name='Body B',
    mode='lines',
    line=dict(width=4)
)

two_body_plot_objects.append(r_b_trace)

two_body_plot_layout = layout = go.Layout(title='Stable Evolution of a Two-Body System in Two-Dimensional Space', paper_bgcolor='#121922',
                                          plot_bgcolor='#121922',
                                          xaxis=dict(title='x (km)',
                                                     range=[-1, 1.5],
                                                     color='white',
                                                     gridcolor='#1b2735'),
                                          yaxis=dict(title='y (km)',
                                                     range=[-0.5, 4.75],
                                                     color='white',
                                                     gridcolor='#1b2735'),
                                          font=dict(color="white")
                                          )

two_body_plot_xy_static_traj = go.Figure(data=two_body_plot_objects,
                                         layout=two_body_plot_layout)

'''
py.plot(two_body_plot_xy_static_traj,
        filename='two_body_plot_xy_static_traj', auto_open=True)
'''

two_body_plot_xy_static_traj.show()


# Animated Trajectory
r_a_trace = go.Scatter(x=r_a_x_sol_[:2],
                       y=r_a_y_sol_[:2],
                       name='Body A',
                       mode='lines',
                       line=dict(width=4))

r_b_trace = go.Scatter(x=r_b_x_sol_[:2],
                       y=r_b_y_sol_[:2],
                       name='Body B',
                       mode='lines',
                       line=dict(width=4))

two_body_plot_trace_frames = [dict(data=[dict(type='scatter',
                                              x=r_a_x_sol_[: r + 1],
                                              y=r_a_y_sol_[: r + 1]),
                                         dict(type='scatter',
                                              x=r_b_x_sol_[: r + 1],
                                              y=r_b_y_sol_[: r + 1])],
                                   traces=[0, 1],
                                   )for r in range(1, len(r_a_x_sol_))]

two_body_plot_layout = go.Layout(title='Stable Evolution of a Two-Body System in Two-Dimensional Space', paper_bgcolor='#121922',
                                 plot_bgcolor='#121922',
                                 xaxis=dict(title='x (km)',
                                            range=[-1, 1.5],
                                            color='white',
                                            gridcolor='#1b2735'),
                                 yaxis=dict(title='y (km)',
                                            range=[-0.5, 4.75],
                                            color='white',
                                            gridcolor='#1b2735'),
                                 updatemenus=[dict(type='buttons',
                                                   font=dict(color='#1b2735'),
                                                   buttons=[dict(label='Play',
                                                                 method='animate',
                                                                 args=[None, dict(frame=dict(
                                                                     duration=3, redraw=False))])])],
                                 font=dict(color="white")
                                 )

two_body_plot_xy_animated_traj = go.Figure(data=[r_a_trace, r_b_trace],
                                           frames=two_body_plot_trace_frames, layout=two_body_plot_layout)

'''
py.plot(two_body_plot_xy_animated_traj,
        filename='two_body_plot_xy_animated_traj', auto_open=True)
'''

two_body_plot_xy_animated_traj.show()
