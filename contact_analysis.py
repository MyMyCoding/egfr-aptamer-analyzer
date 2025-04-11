from Bio.PDB import PDBParser
from io import StringIO

def get_contacts_from_string(pdb_string, cutoff=5.0):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("model", StringIO(pdb_string))
    model = structure[0]
    chains = list(model.get_chains())

    if len(chains) < 2:
        return []

    egfr_atoms = list(chains[0].get_atoms())
    aptamer_atoms = list(chains[1].get_atoms())

    contact_residues = set()
    for egfr_atom in egfr_atoms:
        for apt_atom in aptamer_atoms:
            if egfr_atom - apt_atom < cutoff:
                res = egfr_atom.get_parent()
                contact_residues.add(f"{res.get_resname()}{res.get_id()[1]}")
    return sorted(contact_residues)
