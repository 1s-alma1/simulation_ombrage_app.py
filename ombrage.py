import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Ombrage Photovoltaïque", layout="centered")
st.title("🌤️ Simulation d’ombrage avec pertes estimées (2 obstacles)")

# === Paramètres utilisateur ===
conso_annuelle = 8260  # kWh/an

st.sidebar.header("🔧 Paramètres des obstacles")

# Obstacle 1
st.sidebar.subheader("Obstacle 1 (ex: Arbre)")
h1 = st.sidebar.slider("Hauteur obstacle 1 (m)", 1, 10, 4)
d1 = st.sidebar.slider("Distance obstacle 1 (m)", 1, 20, 5)
t1 = st.sidebar.selectbox("Type obstacle 1", ["Arbre", "Mur", "Bâtiment"], index=0)

# Obstacle 2
st.sidebar.subheader("Obstacle 2 (ex: Bâtiment)")
h2 = st.sidebar.slider("Hauteur obstacle 2 (m)", 1, 15, 6)
d2 = st.sidebar.slider("Distance obstacle 2 (m)", 1, 30, 10)
t2 = st.sidebar.selectbox("Type obstacle 2", ["Aucun", "Bâtiment", "Arbre"], index=1)

# Soleil
hauteur_soleil = st.slider("☀️ Hauteur du soleil (°)", 5, 90, 60)

# === Calcul des ombres ===
ombre1 = h1 / np.tan(np.radians(hauteur_soleil))
ombre2 = h2 / np.tan(np.radians(hauteur_soleil)) if t2 != "Aucun" else 0

# === Maison ===
long_maison = 12
ombre_totale = min(long_maison, ombre1 + ombre2)  # max ombrage limité à la toiture

# === Graphique ===
fig, ax = plt.subplots(figsize=(10, 5))
h_maison = 2.8
toit = np.tan(np.radians(30)) * (long_maison / 2)

# Maison
ax.add_patch(patches.Rectangle((0, 0), long_maison, h_maison, color='lightblue'))
ax.add_patch(patches.Polygon([[0, h_maison], [long_maison/2, h_maison + toit], [long_maison, h_maison]], color='skyblue'))

# Obstacle 1
ax.add_patch(patches.Rectangle((long_maison + d1, 0), 0.8, h1, color='green' if t1=="Arbre" else 'gray'))
ax.text(long_maison + d1, h1 + 0.3, f"{t1} ({h1}m)", fontsize=9)

# Obstacle 2 (si présent)
if t2 != "Aucun":
    ax.add_patch(patches.Rectangle((long_maison + d2, 0), 0.8, h2, color='green' if t2=="Arbre" else 'gray'))
    ax.text(long_maison + d2, h2 + 0.3, f"{t2} ({h2}m)", fontsize=9)

# Ombres projetées
ax.add_patch(patches.Rectangle((long_maison, 0), ombre1, 0.1, color='gray', alpha=0.4))
if t2 != "Aucun":
    ax.add_patch(patches.Rectangle((long_maison + ombre1, 0), ombre2, 0.1, color='gray', alpha=0.3))

# Mise en forme
ax.set_xlim(0, long_maison + max(d1, d2) + 10)
ax.set_ylim(0, 10)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Hauteur (m)")
ax.set_title("Visualisation de l’ombre portée")
ax.grid(True)
st.pyplot(fig)

# === Résultats numériques ===
masquage_pct = round((ombre_totale / long_maison) * 100, 1)
perte_kwh = round((masquage_pct / 100) * conso_annuelle, 1)

st.markdown("### 📊 Résultats de l’analyse")
st.markdown(f"🟫 Longueur d’ombre cumulée sur toiture : **{ombre_totale:.2f} m**")
st.markdown(f"🔧 Taux de masquage estimé : **{masquage_pct:.1f}%**")
st.markdown(f"⚡ Pertes en production estimées : **{perte_kwh:.1f} kWh/an** sur {conso_annuelle} kWh")

st.caption("Simulation simplifiée – pour une validation précise, utiliser PVsyst avec la géométrie exacte.")
