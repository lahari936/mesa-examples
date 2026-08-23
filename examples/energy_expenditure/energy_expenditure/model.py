import mesa
from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid

from .agent import EnergyAgent


class EnergyExpenditureModel(Model):
    """A population of agents that spend energy to move and die when it runs out."""

    def __init__(
        self,
        n=50,
        width=20,
        height=20,
        max_initial_energy=20.0,
        metabolism=0.2,
        move_cost=0.8,
        rest_threshold=3.0,
        rng=None,
    ):
        """Create a new energy expenditure model.

        Args:
            n: Number of agents.
            width, height: Size of the toroidal grid.
            max_initial_energy: Upper bound on an agent's starting energy.
            metabolism: Energy every agent spends per step.
            move_cost: Extra energy an agent spends on a step where it moves.
            rest_threshold: Energy level below which an agent rests.
            rng: Seed for the random number generator.
        """
        super().__init__(rng=rng)

        self.grid = OrthogonalMooreGrid((width, height), torus=True, random=self.random)

        # Starting energy is staggered across the population. With a single
        # shared starting value every agent would die on the same step, which
        # makes the population plot a cliff rather than a decline.
        EnergyAgent.create_agents(
            self,
            n,
            cell=self.random.choices(self.grid.all_cells.cells, k=n),
            energy=[self.random.uniform(1.0, max_initial_energy) for _ in range(n)],
            metabolism=metabolism,
            move_cost=move_cost,
            rest_threshold=rest_threshold,
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Alive": lambda m: len(m.agents),
                "Resting": lambda m: sum(agent.resting for agent in m.agents),
                "Mean Energy": self.mean_energy,
            }
        )
        self.datacollector.collect(self)

    def mean_energy(self):
        """Average energy of the surviving agents, or 0 once they are all gone."""
        if not len(self.agents):
            return 0.0
        return sum(agent.energy for agent in self.agents) / len(self.agents)

    def step(self):
        """Advance the model by one step."""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

        # Nothing replenishes energy, so an empty grid is the end state.
        self.running = len(self.agents) > 0
