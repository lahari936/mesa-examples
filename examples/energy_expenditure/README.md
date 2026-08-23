# Energy Expenditure

A minimal model of agents whose behavior is driven by an internal state rather
than by chance:

> How long does an agent survive when every action costs energy?

Each agent starts with a private energy reserve. Nothing in this world
replenishes it, so the only question an agent answers each step is whether it
can still afford to wander.

## Model behavior

- Every step costs `metabolism` energy, whatever the agent does.
- Moving costs `move_cost` on top of that.
- Below `rest_threshold` the agent rests: it stops moving and pays only
  `metabolism`.
- An agent is removed from the model when its energy reaches zero.

Resting is cheaper, never free. Every agent eventually dies; what differs is
how long each one lasts.

## What to observe

- Agents start with staggered energy levels, so deaths are spread out rather
  than happening all at once.
- The **Alive** curve declines gradually while the **Resting** curve rises and
  then falls as the resting agents die off in turn.
- **Mean Energy** falls quickly at first, then flattens as the survivors are
  increasingly agents that have switched to resting.
- On the grid, agents shift from green to yellow to red before disappearing.

## Why this example

This is the smallest model we could write in which a behavioral switch is
driven purely by an agent's own state. It is meant as a starting point for
resource-constrained models, survival dynamics, and needs-based behavior --
add a food source and the same skeleton becomes a foraging model.

## Files

- `energy_expenditure/agent.py`: the `EnergyAgent` move/rest/die logic.
- `energy_expenditure/model.py`: the grid, the population, and data collection.
- `app.py`: SolaraViz visualization.
- `test_energy_expenditure.py`: checks on the energy and population invariants.

## Run the model

```bash
pip install -r requirements.txt
solara run app.py
```

## Run the tests

```bash
pytest test_energy_expenditure.py
```
