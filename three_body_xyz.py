import numpy as np
from scipy.integrate import odeint

import plotly.graph_objects as go
from plotly.graph_objs import Scatter
import plotly.io as pio
pio.renderers.default = "browser"


'''
import chart_studio
import chart_studio.plotly as py

username = 'lalithuriti'
api_key = 'WkltoYNWP7gEy8eWuRUI'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
'''

G = 6.67428e-11  # Universal Gravitaion Constant | N m^2 kg^-2

m_a = 0.1e9  # Mass - Body A | kg
m_b = 0.6e8  # Mass - Body B | kg
m_c = 0.1e9  # Mass - Body B | kg

r_a = [.1, 0, .4]   # Initial Position - Body A | km
r_b = [0.2, .1, 0]   # Initial Position -  Body B | km
r_c = [-.1, 0, -.1]   # Initial Position -  Body C | km

v_a = [.02, -.02, .08]  # Initial Velocity - Body A | km s^-1
v_b = [.1, .1, -.02]  # Initial Velocity - Body B | km s^-1
v_c = [-.04, -.175, -.01]  # Initial Velocity - Body C | km s^-1


def three_body(init_params, t, G, m_a, m_b, m_c):
    r_a = init_params[:3]
    r_b = init_params[3:6]
    r_c = init_params[6:9]

    v_a = init_params[9:12]
    v_b = init_params[12:15]
    v_c = init_params[15:18]

    r_a_x, r_a_y, r_a_z = r_a
    v_a_x, v_a_y, v_a_z = v_a

    r_b_x, r_b_y, r_b_z = r_b
    v_b_x, v_b_y, v_b_z = v_b

    r_c_x, r_c_y, r_c_z = r_c
    v_c_x, v_c_y, v_c_z = v_c

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

time_span = np.linspace(0, 200, 500)

three_body_sol = odeint(
    three_body, init_params, time_span, args=(G, m_a, m_b, m_c))


r_a_sol = three_body_sol[:, :3]
r_b_sol = three_body_sol[:, 3:6]
r_c_sol = three_body_sol[:, 6:9]

v_a_sol = three_body_sol[:, 9:12]
v_b_sol = three_body_sol[:, 12:15]
v_c_sol = three_body_sol[:, 15:18]


r_a_x_sol = np.array(r_a_sol[:, :1])
r_a_y_sol = np.array(r_a_sol[:, 1:2])
r_a_z_sol = np.array(r_a_sol[:, 2:3])

r_b_x_sol = np.array(r_b_sol[:, :1])
r_b_y_sol = np.array(r_b_sol[:, 1:2])
r_b_z_sol = np.array(r_b_sol[:, 2:3])

r_c_x_sol = np.array(r_c_sol[:, :1])
r_c_y_sol = np.array(r_c_sol[:, 1:2])
r_c_z_sol = np.array(r_c_sol[:, 2:3])


r_a_x_sol_ = r_a_x_sol[:, 0].tolist()
r_a_y_sol_ = r_a_y_sol[:, 0].tolist()
r_a_z_sol_ = r_a_z_sol[:, 0].tolist()

r_b_x_sol_ = r_b_x_sol[:, 0].tolist()
r_b_y_sol_ = r_b_y_sol[:, 0].tolist()
r_b_z_sol_ = r_b_z_sol[:, 0].tolist()

r_c_x_sol_ = r_c_x_sol[:, 0].tolist()
r_c_y_sol_ = r_c_y_sol[:, 0].tolist()
r_c_z_sol_ = r_c_z_sol[:, 0].tolist()


# Static Trajectory
three_body_plot_objects = []

r_a_trace = go.Scatter3d(
    x=r_a_x_sol_,
    y=r_a_y_sol_,
    z=r_a_z_sol_,
    name="Body A",
    mode='lines',
    line=dict(width=4))

three_body_plot_objects.append(r_a_trace)

r_b_trace = go.Scatter3d(
    x=r_b_x_sol_,
    y=r_b_y_sol_,
    z=r_b_z_sol_,
    name='Body B',
    mode='lines',
    line=dict(width=4))

three_body_plot_objects.append(r_b_trace)

r_c_trace = go.Scatter3d(
    x=r_c_x_sol_,
    y=r_c_y_sol_,
    z=r_c_z_sol_,
    name='Body C',
    mode='lines',
    line=dict(width=4))

three_body_plot_objects.append(r_c_trace)

three_body_plot_layout = go.Layout(title='Chaotic Evolution of a Three-Body System in Three-Dimensional Space', paper_bgcolor='#121922',
                                   plot_bgcolor='#121922',
                                   scene=dict(xaxis=dict(title='x (km)',
                                                         backgroundcolor='#121922',
                                                         color='white',
                                                         gridcolor='#1b2735'),
                                              yaxis=dict(title='y (km)',
                                                         backgroundcolor='#121922',
                                                         color='white',
                                                         gridcolor='#1b2735'),
                                              zaxis=dict(title='z (km)',
                                                         backgroundcolor='#121922',
                                                         color='white',
                                                         gridcolor='#1b2735'),
                                              camera=dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
                                                          eye=dict(x=-1.25, y=-1.25, z=1.25))),
                                   font=dict(color="white")
                                   )

three_body_plot_xyz_static_traj = go.Figure(data=three_body_plot_objects,
                                            layout=three_body_plot_layout)

'''py.plot(three_body_plot_xyz_static_traj,
        filename='three_body_plot_xyz_static_traj', auto_open=True)'''

three_body_plot_xyz_static_traj.show()


# Animated Trajectory
r_a_trace = go.Scatter3d(x=r_a_x_sol_[:2],
                         y=r_a_y_sol_[:2],
                         z=r_a_z_sol_[:2],
                         name='Body A',
                         mode='lines',
                         line=dict(width=4))

r_b_trace = go.Scatter3d(x=r_b_x_sol_[:2],
                         y=r_b_y_sol_[:2],
                         z=r_b_z_sol_[:2],
                         name='Body B',
                         mode='lines',
                         line=dict(width=4))

r_c_trace = go.Scatter3d(x=r_c_x_sol_[:2],
                         y=r_c_y_sol_[:2],
                         z=r_c_z_sol_[:2],
                         name='Body C',
                         mode='lines',
                         line=dict(width=4))

three_body_plot_trace_frames = [dict(data=[dict(type='scatter3d',
                                                x=r_a_x_sol_[: r + 1],
                                                y=r_a_y_sol_[: r + 1],
                                                z=r_a_z_sol_[: r + 1]),
                                           dict(type='scatter3d',
                                                x=r_b_x_sol_[: r + 1],
                                                y=r_b_y_sol_[: r + 1],
                                                z=r_b_z_sol_[: r + 1]),
                                           dict(type='scatter3d',
                                                x=r_c_x_sol_[: r + 1],
                                                y=r_c_y_sol_[: r + 1],
                                                z=r_c_z_sol_[: r + 1])],
                                     traces=[0, 1, 2],
                                     )for r in range(1, len(r_a_x_sol_))]

three_body_plot_layout = go.Layout(title='Chaotic Evolution of a Three-Body System in Three-Dimensional Space', paper_bgcolor='#121922',
                                   plot_bgcolor='#121922',
                                   scene=dict(xaxis=dict(title='x (km)',
                                                         backgroundcolor='#121922',
                                                         color='white',
                                                         gridcolor='#1b2735'),
                                              yaxis=dict(title='y (km)',
                                                         backgroundcolor='#121922',
                                                         color='white',
                                                         gridcolor='#1b2735'),
                                              zaxis=dict(title='z (km)',
                                                         backgroundcolor='#121922',
                                                         color='white',
                                                         gridcolor='#1b2735'),
                                              camera=dict(
                                                up=dict(x=0, y=0, z=9),
                                                center=dict(x=0, y=0, z=0),
                                                eye=dict(x=-1.25, y=-1.25, z=1.25))),
                                   updatemenus=[dict(type='buttons',
                                                     font=dict(
                                                         color='#1b2735'),
                                                     buttons=[dict(label='Play',
                                                                   method='animate',
                                                                   args=[None, dict(
                                                                       frame=dict(duration=3))])])],
                                   font=dict(color="white")
                                   )

three_body_plot_xyz_animated_traj = go.Figure(data=[r_a_trace, r_b_trace, r_c_trace],
                                              frames=three_body_plot_trace_frames, layout=three_body_plot_layout)

'''
py.plot(three_body_plot_xyz_animated_traj,
        filename='three_body_plot_xyz_animated_traj', auto_open=True)
'''

three_body_plot_xyz_animated_traj.show()
