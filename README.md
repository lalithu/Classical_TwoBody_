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
