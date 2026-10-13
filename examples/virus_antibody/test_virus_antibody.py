"""Regression tests for the virus antibody model."""

from virus_antibody.agents import VirusAgent
from virus_antibody.model import VirusAntibodyModel


def test_model_builds_with_defaults():
    """The default model must build.

    `create_agents` broadcasts a list, tuple or array as one value per agent and
    rejects a length mismatch, so passing a single 3-gene dna for 20 viruses
    raised ValueError.
    """
    model = VirusAntibodyModel()

    viruses = model.agents_by_type[VirusAgent]
    assert len(viruses) == model.initial_viruses


def test_each_virus_has_its_own_dna():
    """Viruses start from one strain but must not share a single dna list."""
    model = VirusAntibodyModel(initial_viruses=10, rng=1)
    viruses = list(model.agents_by_type[VirusAgent])

    first = viruses[0]
    assert all(v.dna == first.dna for v in viruses), "all viruses share a strain"
    assert len({id(v.dna) for v in viruses}) == len(viruses), (
        "viruses share one dna list object"
    )

    first.dna[0] = (first.dna[0] + 1) % 10
    assert any(v.dna != first.dna for v in viruses[1:]), (
        "mutating one virus changed the others"
    )


def test_duplication_leaves_the_parent_genome_alone():
    """generate_dna() must not rewrite the genome it is handed."""
    model = VirusAntibodyModel(initial_viruses=1, rng=2)
    parent = next(iter(model.agents_by_type[VirusAgent]))
    parent.mutation_rate = 1.0  # force a mutation
    before = parent.dna.copy()

    child_dna = parent.generate_dna(parent.dna)

    assert parent.dna == before, "parent genome was mutated in place"
    assert child_dna is not parent.dna, "child shares the parent's dna list"


def test_model_runs():
    """A short run must not raise."""
    model = VirusAntibodyModel(initial_viruses=5, initial_antibody=5, rng=3)
    model.run_for(10)
    assert model.time == 10.0
