"""Solara visualization for the Energy Expenditure model."""

from energy_expenditure.model import EnergyExpenditureModel
from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle


def agent_portrayal(agent):
    """Green = comfortable, yellow = running low, red = resting."""
    if agent.resting:
        color = "#e74c3c"
    elif agent.energy > 3 * agent.rest_threshold:
        color = "#2ecc71"
    else:
        color = "#f1c40f"
    return AgentPortrayalStyle(color=color, size=30)


model_params = {
    "rng": {
        "type": "InputText",
        "value": 42,
        "label": "Random seed",
    },
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents",
        "min": 10,
        "max": 300,
        "step": 10,
    },
    "max_initial_energy": {
        "type": "SliderFloat",
        "value": 20.0,
        "label": "Max initial energy",
        "min": 5.0,
        "max": 50.0,
        "step": 1.0,
    },
    "metabolism": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Metabolism (cost per step)",
        "min": 0.05,
        "max": 1.0,
        "step": 0.05,
    },
    "move_cost": {
        "type": "SliderFloat",
        "value": 0.8,
        "label": "Extra cost of moving",
        "min": 0.0,
        "max": 2.0,
        "step": 0.1,
    },
    "rest_threshold": {
        "type": "SliderFloat",
        "value": 3.0,
        "label": "Rest below this energy",
        "min": 0.0,
        "max": 15.0,
        "step": 0.5,
    },
    "width": 20,
    "height": 20,
}

model = EnergyExpenditureModel(rng=42)

renderer = SpaceRenderer(model=model, backend="matplotlib").render(
    agent_portrayal=agent_portrayal
)

population_plot = make_plot_component({"Alive": "#2c3e50", "Resting": "#e74c3c"})
energy_plot = make_plot_component("Mean Energy")

page = SolaraViz(
    model,
    renderer,
    components=[population_plot, energy_plot],
    model_params=model_params,
    name="Energy Expenditure",
)
