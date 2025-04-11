import streamlit as st
import pandas as pd
from contact_analysis import get_contacts_from_string

st.title("🧬 Upload PDB Files to Analyze EGFR–Aptamer Contacts")

uploaded_files = st.file_uploader("Upload one or more PDB files", type="pdb", accept_multiple_files=True)

if not uploaded_files:    
    st.info("👆 Upload some .pdb files to begin.")
    st.stop()

contact_map = {}

with st.spinner("Analyzing uploaded files..."):
    for file in uploaded_files:
        try:
            pdb_string = file.getvalue().decode("utf-8")
            contacts = get_contacts_from_string(pdb_string)
            model_name = file.name.replace(".pdb", "")
            contact_map[model_name] = contacts
            st.success(f"✅ {file.name} analyzed ({len(contacts)} contacts)")
        except Exception as e:
            st.error(f"❌ {file.name}: {e}")

if not contact_map:
    st.warning("No valid contact data found.")
    st.stop()

all_residues = sorted(set(r for res in contact_map.values() for r in res))
df = pd.DataFrame(index=all_residues)

for model, contacts in contact_map.items():
    df[model] = [res in contacts for res in all_residues]

st.subheader("📊 Contact Residue Table")
st.dataframe(df.astype(bool))
st.download_button("📥 Download CSV", df.to_csv().encode(), file_name="contact_comparison.csv")
