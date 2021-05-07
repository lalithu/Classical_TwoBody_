import numpy as np
from scipy.integrate import odeint

import plotly.graph_objects as go
from plotly.graph_objs import Scatter

'''
import chart_studio
import chart_studio.plotly as py

username = 'lalithuriti'
api_key = '··············'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
'''

G = 1  # Universal Gravitaion Constant |

m_a = 0.1e1  # Mass - Body A |
m_b = 0.1e1  # Mass - Body B |
m_c = 0.1e1  # Mass - Body B |

x1 = -0.97000436
y1 = 0.24308753
r_a = [x1, y1]   # Initial Position - Body A |
r_b = [-x1, -y1]   # Initial Position -  Body B |
r_c = [0, 0]   # Initial Position -  Body C |

vx3 = 0.93240737
vy3 = 0.86473146
v_a = [-vx3 / 2, -vy3 / 2]  # Initial Velocity - Body A |
v_b = [-vx3 / 2, -vy3 / 2]  # Initial Velocity - Body B |
v_c = [vx3, vy3]  # Initial Velocity - Body C |


def three_body(init_params, t, G, m_a, m_b, m_c):
    r_a = init_params[:2]
    r_b = init_params[2:4]
    r_c = init_params[4:6]

    v_a = init_params[6:8]
    v_b = init_params[8:10]
    v_c = init_params[10:12]

    r_a_x, r_a_y = r_a
    v_a_x, v_a_y = v_a

    r_b_x, r_b_y = r_b
    v_b_x, v_b_y = v_b

    r_c_x, r_c_y = r_c
    v_c_x, v_c_y = v_c

    r_ab = np.linalg.norm(r_b - r_a)
    r_bc = np.linalg.norm(r_c - r_b)
    r_ca = np.linalg.norm(r_a - r_c)

    # Position | ∫dx/dt
    dr_a_dt = v_a
    dr_b_dt = v_b
    dr_c_dt = v_c

    # Velocity | ∫dv/dt
    dv_a_dt = (G * m_b * ((r_b - r_a) / r_ab) / r_ab ** 2) + \
        (G * m_c * ((r_c - r_a) / r_ca) / r_ca ** 2)

    dv_b_dt = (G * m_a * ((r_a - r_b) / r_ab) / r_ab ** 2) + \
        (G * m_c * ((r_c - r_b) / r_bc) / r_bc ** 2)

    dv_c_dt = (G * m_a * ((r_a - r_c) / r_ca) / r_ca ** 2) + \
        (G * m_b * ((r_b - r_c) / r_bc) / r_bc ** 2)

    return np.array([dr_a_dt, dr_b_dt, dr_c_dt, dv_a_dt, dv_b_dt, dv_c_dt]).flatten()


init_params = np.array([r_a, r_b, r_c, v_a, v_b, v_c]).flatten()
print(init_params)

time_span = np.linspace(0, 20, 800)

two_body_sol = odeint(
    three_body, init_params, time_span, args=(G, m_a, m_b, m_c))


r_a_sol = two_body_sol[:, :2]
r_b_sol = two_body_sol[:, 2:4]
r_c_sol = two_body_sol[:, 4:6]

v_a_sol = two_body_sol[:, 6:8]
v_b_sol = two_body_sol[:, 8:10]
v_b_sol = two_body_sol[:, 10:12]


r_a_x_sol = np.array(r_a_sol[:, :1])
r_a_y_sol = np.array(r_a_sol[:, 1:2])

r_b_x_sol = np.array(r_b_sol[:, :1])
r_b_y_sol = np.array(r_b_sol[:, 1:2])

r_c_x_sol = np.array(r_c_sol[:, :1])
r_c_y_sol = np.array(r_c_sol[:, 1:2])


r_a_x_sol_ = r_a_x_sol[:, 0].tolist()
r_a_y_sol_ = r_a_y_sol[:, 0].tolist()

r_b_x_sol_ = r_b_x_sol[:, 0].tolist()
r_b_y_sol_ = r_b_y_sol[:, 0].tolist()

r_c_x_sol_ = r_c_x_sol[:, 0].tolist()
r_c_y_sol_ = r_c_y_sol[:, 0].tolist()


# Static Trajectory
three_body_plot_objects = []

r_a_trace = go.Scatter(
    x=r_a_x_sol_,
    y=r_a_y_sol_,
    name="Body A",
    mode='lines',
    line=dict(width=8))

three_body_plot_objects.append(r_a_trace)

r_b_trace = go.Scatter(
    x=r_b_x_sol_,
    y=r_b_y_sol_,
    name='Body B',
    mode='lines',
    line=dict(width=6))

three_body_plot_objects.append(r_b_trace)

r_c_trace = go.Scatter(
    x=r_c_x_sol_,
    y=r_c_y_sol_,
    name='Body C',
    mode='lines',
    line=dict(width=4))

three_body_plot_objects.append(r_c_trace)

three_body_plot_layout = go.Layout(title='Stable Evolution of a Three-Body System in Three-Dimensional Space', paper_bgcolor='#121922',
                                   plot_bgcolor='#121922',
                                   xaxis=dict(title='x (km)',
                                              color='white',
                                              gridcolor='#1b2735'),
                                   yaxis=dict(title='y (km)',
                                              color='white',
                                              gridcolor='#1b2735'),
                                   font=dict(color="white")
                                   )

three_body_plot_xy_static_traj = go.Figure(data=three_body_plot_objects,
                                           layout=three_body_plot_layout)

'''
py.plot(two_body_plot_xyz_static_traj,
        filename='two_body_plot_xyz_static_traj', auto_open=True)
'''

three_body_plot_xy_static_traj.show()


# Animated Trajectory
r_a_trace = go.Scatter(x=r_a_x_sol_[:1],
                       y=r_a_y_sol_[:1],
                       name='Body A',
                       mode='markers',
                       marker=dict(size=20))

r_b_trace = go.Scatter(x=r_b_x_sol_[:1],
                       y=r_b_y_sol_[:1],
                       name='Body B',
                       mode='markers',
                       marker=dict(size=20))

r_c_trace = go.Scatter(x=r_c_x_sol_[:1],
                       y=r_c_y_sol_[:1],
                       name='Body C',
                       mode='markers',
                       marker=dict(size=20))

r_path = go.Scatter(
    x=r_c_x_sol_,
    y=r_c_y_sol_,
    name='',
    showlegend=False,
    mode='lines',
    line=dict(width=1))

three_body_plot_trace_frames = [dict(data=[dict(type='scatter',
                                                x=r_a_x_sol_[r - 1: r],
                                                y=r_a_y_sol_[r - 1: r]),
                                           dict(type='scatter',
                                                x=r_b_x_sol_[r - 1: r],
                                                y=r_b_y_sol_[r - 1: r]),
                                           dict(type='scatter',
                                                x=r_c_x_sol_[r - 1: r],
                                                y=r_c_y_sol_[r - 1: r])],
                                     traces=[1, 2, 3],
                                     )for r in range(1, len(r_a_x_sol_))]

three_body_plot_layout = go.Layout(title='Stable Evolution of a Three-Body System in Three-Dimensional Space', paper_bgcolor='#121922',
                                   plot_bgcolor='#121922',
                                   xaxis=dict(title='x (km)',
                                              range=[-1.25, 1.25],
                                              color='white',
                                              gridcolor='#1b2735'),
                                   yaxis=dict(title='y (km)',
                                              range=[-.5, .5],
                                              color='white',
                                              gridcolor='#1b2735'),
                                   updatemenus=[dict(type='buttons',
                                                     font=dict(
                                                         color='#1b2735'),
                                                     buttons=[dict(label='Play',
                                                                   method='animate',
                                                                   args=[None, dict(
                                                                       frame=dict(duration=3))])])],
                                   font=dict(color="white")
                                   )

three_body_plot_xy_animated_traj = go.Figure(data=[r_path, r_a_trace, r_b_trace, r_c_trace],
                                             frames=three_body_plot_trace_frames, layout=three_body_plot_layout)

'''
py.plot(two_body_plot_xyz_animated_traj,
           filename='two_body_plot_xyz_animated_traj', auto_open=True)
'''

three_body_plot_xy_animated_traj.show()
