import streamlit as st
import pandas as pd
import os
from contact_analysis import get_contacts

st.title("🧬 EGFR–Aptamer Contact Comparison")

pdb_dir = "data"
pdb_files = [f for f in os.listdir(pdb_dir) if f.endswith(".pdb")]

if not pdb_files:
    st.warning("No PDB files found in 'data/' folder.")
    st.stop()

contact_map = {}

with st.spinner("Analyzing contact residues..."):
    for pdb_file in pdb_files:
        model_name = pdb_file.replace(".pdb", "")
        contacts = get_contacts(os.path.join(pdb_dir, pdb_file))
        contact_map[model_name] = contacts

all_residues = sorted(set(r for res in contact_map.values() for r in res))
df = pd.DataFrame(index=all_residues)

for model, contacts in contact_map.items():
    df[model] = [res in contacts for res in all_residues]

st.dataframe(df.astype(bool))
st.download_button("Download CSV", df.to_csv().encode(), file_name="contact_comparison.csv")
