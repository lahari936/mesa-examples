from mesa.discrete_space import CellAgent


class EnergyAgent(CellAgent):
    """An agent whose behavior is driven by how much energy it has left.

    Every step costs ``metabolism`` energy just to stay alive. Wandering costs
    ``move_cost`` on top of that, so an agent that keeps moving burns through
    its reserve much faster than one that sits still. Once energy drops below
    ``rest_threshold`` the agent rests instead of moving, which is cheaper but
    never free -- there is no food in this world, so every agent eventually
    dies. What differs is how long each one lasts.

    Attributes:
        energy: Remaining energy. The agent is removed when it hits zero.
        metabolism: Energy spent every step regardless of what the agent does.
        move_cost: Extra energy spent on a step where the agent moves.
        rest_threshold: Energy level below which the agent rests instead of moving.
    """

    def __init__(
        self,
        model,
        cell,
        energy=20.0,
        metabolism=0.2,
        move_cost=0.8,
        rest_threshold=3.0,
    ):
        """Create an agent.

        Args:
            model: The model instance.
            cell: The starting cell of the agent.
            energy: Starting energy.
            metabolism: Energy spent every step.
            move_cost: Extra energy spent when moving.
            rest_threshold: Energy level below which the agent rests.
        """
        super().__init__(model)
        self.cell = cell
        self.energy = energy
        self.metabolism = metabolism
        self.move_cost = move_cost
        self.rest_threshold = rest_threshold

    @property
    def resting(self):
        """True when the agent is too low on energy to keep wandering."""
        return self.energy < self.rest_threshold

    def step(self):
        """Move or rest, pay for it, and die if the reserve is empty."""
        cost = self.metabolism

        if not self.resting:
            self.cell = self.cell.neighborhood.select_random_cell()
            cost += self.move_cost

        # Energy is only ever spent here, so the decision above and the
        # bookkeeping stay in one place and energy strictly decreases.
        self.energy = max(self.energy - cost, 0.0)

        if self.energy == 0.0:
            self.remove()
