# Agent-Based Micro-Economy: FSM Behavior Engine

A Python-based conceptual framework designed to model complex automated systems. This engine uses a custom Finite State Machine (FSM) to simulate a localized economy, generating synthetic behavioral data for 50 independent agents over a 48-hour cycle.

## The Architecture & MVP Constraints
To rigorously test the FSM logic and ensure perfect synchronization between the Pandas data logging and the spatial environment, this model is intentionally constrained to a two-node micro-economy (Factory and Store). This allowed for the precise debugging of coordinate collisions and logic loops without the noise of an overbuilt environment. 

The system is separated into three distinct modules:

1. **The FSM Engine (`simulator.py`) — *Engineered from scratch***
   Drives deterministic agent logic (Working, Shopping, Sleeping, Travelling) based on randomized class tiers and wage metrics. Handles spatial routing and logs exact grid coordinates, wealth accumulation, and state changes to a Pandas matrix.
2. **The Analytics (`city_analysis.py`) — *Engineered from scratch***
   A Seaborn-powered data visualization script that analyzes the generated `simulation_data.csv` to prove the underlying socio-economic logic, tracking wealth disparities between Poverty, Middle, and Upper-class agents over time.
3. **The Rendering Pipeline (`sim_render.py`) — *AI-Assisted***
   Because the primary focus of this project is backend system architecture, I leveraged AI to help construct a custom Matplotlib `FuncAnimation` pipeline. This bypasses standard web-based categorical trace limits and visually reconstructs the data matrix frame-by-frame.

## Installation & Execution

```bash

# Clone the repository
git clone https://github.com/Vanshbits/Micro-Economy-Engine.git
cd Micro-Economy-Engine

# Install dependencies
pip install -r requirements.txt

# Step 1: Run the simulation
python simulator.py

# Step 2: Render the environment (Exports animation / displays interactive window & Generates simulation_data.csv)
python sim_render.py

# Step 3: View the analytics (Displays the wealth distribution graph)
python city_analysis.py
