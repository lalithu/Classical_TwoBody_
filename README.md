# 🪐 Classical Two-Body  
**An elementary analysis and visualization of the classical two-body problem using Python and Plotly**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Graphing%20Library-orange.svg)](https://plotly.com/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with SciPy](https://img.shields.io/badge/Made%20with-SciPy-red.svg)](https://scipy.org/)

---

## 🧭 Overview
This project numerically integrates Newton’s equations of motion for a two-body gravitational system  
and visualizes the results interactively using **Plotly**.  
It provides an accessible, browser-based approach to exploring **orbital mechanics** through modern computational tools.

---

## ⚙️ Features
- 🧮 Solves two-body motion using `scipy.integrate.odeint`  
- 🎨 Interactive 2D and 3D Plotly visualizations  
- 🔄 Animated trajectories and static plots  
- 🧠 Object-oriented design for easy customization  
- 📈 Uses physical constants (SI units, configurable `G`)  

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/<your-username>/Classical_TwoBody_.git
cd Classical_TwoBody_

# Install dependencies
pip install numpy scipy plotly

# Run the simulation
python two_body_class.py


📘 Mathematical Formulation

The motion of two bodies under mutual gravitation is governed by Newton’s Law of Universal Gravitation.

The force between two masses is given by:

F = G · (m₁ · m₂) / r²

where:

F — gravitational force (N)

G — gravitational constant (6.674 × 10⁻¹¹ N·m²·kg⁻²)

m₁, m₂ — masses of the two bodies (kg)

r — distance between their centers (m)

In vector form, the acceleration of each body is determined by:

a₁ = G · m₂ · (r₂ − r₁) / |r₂ − r₁|³
a₂ = G · m₁ · (r₁ − r₂) / |r₁ − r₂|³

Combining these equations gives the coupled second-order differential system:

d²r₁/dt² = G · m₂ · (r₂ − r₁) / |r₂ − r₁|³
d²r₂/dt² = G · m₁ · (r₁ − r₂) / |r₁ − r₂|³

In this project, these equations are numerically integrated over time using the
scipy.integrate.odeint solver, which computes the position and velocity of each body
at discrete time steps, enabling a complete simulation of their orbital evolution.



🧩 Example Usage
from two_body_class import two_body

bodies = [
    {
        'Name': 'A',
        'Mass': 1e10,
        'init_position': [-0.5, 0],
        'init_velocity': [0.02, 0.1],
        'Radius': 0.12,
        'Color': 'dodgerblue',
        'Color_Gradient': 'mediumseagreen'
    },
    {
        'Name': 'B',
        'Mass': 1e6,
        'init_position': [0.5, 0],
        'init_velocity': [-0.08, -0.06],
        'Radius': 0.1,
        'Color': 'darkred',
        'Color_Gradient': 'crimson'
    }
]

sim = two_body(bodies, time_span=36, G=6.67428e-11)
sim.plot()


🧠 Concepts Explored

Newtonian gravitation and relative motion

Numerical integration of coupled differential equations

Orbital dynamics and system stability

Interactive data visualization in scientific computing

📂 Project Structure
File	Description
two_body_class.py	Object-oriented two-body simulator (with static and animated Plotly visualization)
two_body_2D.py	Basic 2D implementation of the classical two-body problem
two_body_3D.py	Three-dimensional orbital visualization
three_body_2D.py	Extended two-dimensional three-body problem
three_body_3D.py	Chaotic 3D three-body dynamics visualization
🧰 Dependencies

Install the required libraries manually:

pip install numpy scipy plotly


or via a requirements file:

pip install -r requirements.txt


Core dependencies:

NumPy
 — for numerical computation

SciPy
 — for ODE integration (odeint)

Plotly
 — for interactive 2D and 3D visualization

🧑‍💻 Author

Lalith Uriti
Developer & Researcher in Computational Mechanics and Visualization

📧 lalithuriti@gmail.com

🌐 LinkedIn
 • GitHub

📜 License

Released under the MIT License
.
© 2025 Lalith Uriti — feel free to use, modify, and build upon this work.

🌌 Acknowledgements

This project was inspired by the elegance of classical mechanics and the goal of making orbital motion more accessible through visualization.
Special thanks to the open-source Python community for providing the tools that made this project possible.
Gratitude to Plotly, NumPy, and SciPy for enabling interactive and educational scientific computing experiences.