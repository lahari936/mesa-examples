from energy_expenditure.model import EnergyExpenditureModel


def test_energy_never_increases():
    """Nothing in the model replenishes energy, so every agent's reserve must
    be monotonically non-increasing."""
    model = EnergyExpenditureModel(n=30, rng=1)
    previous = {agent.unique_id: agent.energy for agent in model.agents}

    for _ in range(30):
        model.step()
        for agent in model.agents:
            assert agent.energy <= previous[agent.unique_id]
            previous[agent.unique_id] = agent.energy


def test_population_dies_off_gradually():
    """Staggered starting energy means the population should shrink over
    several steps rather than emptying all at once."""
    model = EnergyExpenditureModel(n=50, rng=2)
    counts = [len(model.agents)]

    while model.running and len(counts) < 500:
        model.step()
        counts.append(len(model.agents))

    assert counts[-1] == 0, "every agent should eventually run out of energy"
    assert all(later <= earlier for earlier, later in zip(counts, counts[1:]))

    steps_with_deaths = sum(
        1 for earlier, later in zip(counts, counts[1:]) if later < earlier
    )
    assert steps_with_deaths > 1, "the whole population died on a single step"


def test_low_energy_agents_rest_instead_of_moving():
    """An agent below the rest threshold stays put."""
    model = EnergyExpenditureModel(n=1, rest_threshold=100.0, rng=3)
    agent = next(iter(model.agents))
    start_cell = agent.cell
    start_energy = agent.energy

    agent.step()

    assert agent.resting
    assert agent.cell is start_cell
    assert agent.energy == start_energy - agent.metabolism


def test_dead_agents_leave_the_grid():
    """A removed agent must not linger in the cell it died in."""
    model = EnergyExpenditureModel(n=20, max_initial_energy=2.0, rng=4)
    model.run_for(20)

    assert len(model.agents) == 0
    assert sum(len(cell.agents) for cell in model.grid.all_cells) == 0
