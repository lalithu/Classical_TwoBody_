import numpy as np
from scipy.integrate import odeint

import plotly.graph_objects as go
from plotly.graph_objs import Scatter
import plotly.io as pio
pio.renderers.default = "browser"

'''
Optional: Chart Studio Configuration
-----------------------------------
Uncomment this block if you wish to upload your visualizations
to a Plotly Chart Studio account. It is not required for local use.
'''
# import chart_studio
# import chart_studio.plotly as py
# username = 'lalithuriti'
# api_key = 'WkltoYNWP7gEy8eWuRUI'
# chart_studio.tools.set_credentials_file(username=username, api_key=api_key)


# ------------------------------------------------------------
# Physical Constants and Initial Conditions
# ------------------------------------------------------------

G = 6.67428e-11  # Universal Gravitational Constant | N·m²·kg⁻²

# Masses of the two bodies (in kilograms)
m_a = 0.1e10  # Body A
m_b = 0.1e6   # Body B

# Initial positions (in meters)
r_a = [-0.5, 0, 1]   # Body A
r_b = [0.5, 0, -1]   # Body B

# Initial velocities (in meters per second)
v_a = [0.02, 0.1, 0.04]   # Body A
v_b = [0.08, -0.1, 0.04]  # Body B


# ------------------------------------------------------------
# Two-Body System Differential Equations
# ------------------------------------------------------------

def two_body(init_params, t, G, m1, m2):
    """
    Defines the differential equations for a two-body gravitational system
    in three-dimensional space.

    Parameters
    ----------
    init_params : ndarray
        Flattened array containing initial positions and velocities:
        [r_a, r_b, v_a, v_b]
    t : float
        Time variable (required by odeint, unused directly)
    G : float
        Gravitational constant
    m1, m2 : float
        Masses of the two bodies

    Returns
    -------
    ndarray
        Flattened array of time derivatives (position and velocity)
    """

    # Unpack position and velocity components
    r_a = init_params[:3]
    r_b = init_params[3:6]
    v_a = init_params[6:9]
    v_b = init_params[9:12]

    # Decompose vectors (for clarity)
    r_a_x, r_a_y, r_a_z = r_a
    v_a_x, v_a_y, v_a_z = v_a
    r_b_x, r_b_y, r_b_z = r_b
    v_b_x, v_b_y, v_b_z = v_b

    # Compute distance between bodies
    r = np.linalg.norm(r_a - r_b)

    # Position derivatives (velocities)
    dr_a_dt = v_a
    dr_b_dt = v_b

    # Velocity derivatives (accelerations from gravity)
    dv_a_dt = G * m_b * ((r_b - r_a) / r) / r ** 2
    dv_b_dt = G * m_a * ((r_a - r_b) / r) / r ** 2

    # Return flattened array of derivatives
    return np.array([dr_a_dt, dr_b_dt, dv_a_dt, dv_b_dt]).flatten()


# ------------------------------------------------------------
# Numerical Integration Setup
# ------------------------------------------------------------

# Combine initial positions and velocities into one vector
init_params = np.array([r_a, r_b, v_a, v_b]).flatten()
print(init_params)

# Define time range for simulation
time_span = np.linspace(0, 480, 600)

# Solve differential equations using SciPy's ODE integrator
two_body_sol = odeint(two_body, init_params, time_span, args=(G, m_a, m_b))

# Extract positions and velocities for each body
r_a_sol = two_body_sol[:, :3]
r_b_sol = two_body_sol[:, 3:6]
v_a_sol = two_body_sol[:, 6:9]
v_b_sol = two_body_sol[:, 9:12]


# ------------------------------------------------------------
# Prepare Data for Visualization
# ------------------------------------------------------------

# Position components (X, Y, Z) for both bodies
r_a_x_sol = np.array(r_a_sol[:, :1])
r_a_y_sol = np.array(r_a_sol[:, 1:2])
r_a_z_sol = np.array(r_a_sol[:, 2:3])

r_b_x_sol = np.array(r_b_sol[:, :1])
r_b_y_sol = np.array(r_b_sol[:, 1:2])
r_b_z_sol = np.array(r_b_sol[:, 2:3])

# Convert to Python lists for Plotly compatibility
r_a_x_sol_ = r_a_x_sol[:, 0].tolist()
r_a_y_sol_ = r_a_y_sol[:, 0].tolist()
r_a_z_sol_ = r_a_z_sol[:, 0].tolist()

r_b_x_sol_ = r_b_x_sol[:, 0].tolist()
r_b_y_sol_ = r_b_y_sol[:, 0].tolist()
r_b_z_sol_ = r_b_z_sol[:, 0].tolist()


# ------------------------------------------------------------
# Static 3D Trajectory Visualization
# ------------------------------------------------------------

two_body_plot_objects = []

# Body A trajectory
r_a_trace = go.Scatter3d(
    x=r_a_x_sol_,
    y=r_a_y_sol_,
    z=r_a_z_sol_,
    name="Body A",
    mode='lines',
    line=dict(width=4))
two_body_plot_objects.append(r_a_trace)

# Body B trajectory
r_b_trace = go.Scatter3d(
    x=r_b_x_sol_,
    y=r_b_y_sol_,
    z=r_b_z_sol_,
    name='Body B',
    mode='lines',
    line=dict(width=4))
two_body_plot_objects.append(r_b_trace)

# Layout styling for 3D static visualization
two_body_plot_layout = go.Layout(
    title='Stable Evolution of a Two-Body System in Three-Dimensional Space',
    paper_bgcolor='#121922',
    plot_bgcolor='#121922',
    scene=dict(
        xaxis=dict(title='x (km)', backgroundcolor='#121922', color='white', gridcolor='#1b2735'),
        yaxis=dict(title='y (km)', backgroundcolor='#121922', color='white', gridcolor='#1b2735'),
        zaxis=dict(title='z (km)', backgroundcolor='#121922', color='white', gridcolor='#1b2735'),
        camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=-1.25, z=1.25)
        )
    ),
    font=dict(color="white")
)

# Combine data and layout into figure
two_body_plot_xyz_static_traj = go.Figure(
    data=two_body_plot_objects,
    layout=two_body_plot_layout
)

# Display static trajectory
two_body_plot_xyz_static_traj.show()


# ------------------------------------------------------------
# Animated 3D Trajectory Visualization
# ------------------------------------------------------------

# Initial traces (first few points)
r_a_trace = go.Scatter3d(
    x=r_a_x_sol_[:2],
    y=r_a_y_sol_[:2],
    z=r_a_z_sol_[:2],
    name='Body A',
    mode='lines',
    line=dict(width=4)
)

r_b_trace = go.Scatter3d(
    x=r_b_x_sol_[:2],
    y=r_b_y_sol_[:2],
    z=r_b_z_sol_[:2],
    name='Body B',
    mode='lines',
    line=dict(width=4)
)

# Create animation frames (incremental updates per time step)
two_body_plot_trace_frames = [
    dict(data=[
        dict(type='scatter3d', x=r_a_x_sol_[:r + 1], y=r_a_y_sol_[:r + 1], z=r_a_z_sol_[:r + 1]),
        dict(type='scatter3d', x=r_b_x_sol_[:r + 1], y=r_b_y_sol_[:r + 1], z=r_b_z_sol_[:r + 1])
    ],
    traces=[0, 1])
    for r in range(1, len(r_a_x_sol_))
]

# Layout configuration for animated figure
two_body_plot_layout = go.Layout(
    title='Stable Evolution of a Two-Body System in Three-Dimensional Space',
    paper_bgcolor='#121922',
    plot_bgcolor='#121922',
    scene=dict(
        xaxis=dict(title='x (km)', backgroundcolor='#121922', color='white', gridcolor='#1b2735'),
        yaxis=dict(title='y (km)', backgroundcolor='#121922', color='white', gridcolor='#1b2735'),
        zaxis=dict(title='z (km)', backgroundcolor='#121922', color='white', gridcolor='#1b2735')
    ),
    updatemenus=[dict(
        type='buttons',
        font=dict(color='#1b2735'),
        buttons=[dict(
            label='Play',
            method='animate',
            args=[None, dict(frame=dict(duration=3))]
        )]
    )],
    font=dict(color="white")
)

# Combine traces, frames, and layout into animation
two_body_plot_xyz_animated_traj = go.Figure(
    data=[r_a_trace, r_b_trace],
    frames=two_body_plot_trace_frames,
    layout=two_body_plot_layout
)

# Display animated trajectory
two_body_plot_xyz_animated_traj.show()
