import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
pip install matplotlib
pip install numpy


st.set_page_config(page_title="Simulation d’Ombrage PV", layout="centered")
st.title("☀️ Simulation d’ombrage sur une maison photovoltaïque")

# Entrées utilisateur
obstacle = st.selectbox("Choisissez le type d’obstacle", ["Arbre", "Bâtiment", "Mur"])
hauteur_obstacle = st.slider("Hauteur de l’obstacle (m)", 1, 10, 4)
distance_obstacle = st.slider("Distance de l’obstacle depuis la maison (m)", 1, 20, 5)
hauteur_soleil = st.slider("Hauteur du soleil (°)", 5, 90, 60)

# Calcul de l’ombre
longueur_ombre = hauteur_obstacle / np.tan(np.radians(hauteur_soleil))

# Affichage graphique
fig, ax = plt.subplots(figsize=(10, 5))
longueur_maison = 12
hauteur_maison = 2.8
inclinaison_deg = 30

# Maison
ax.add_patch(patches.Rectangle((0, 0), longueur_maison, hauteur_maison, facecolor='lightblue', label="Maison"))
ax.add_patch(patches.Polygon([[0, hauteur_maison],
                              [longueur_maison / 2, hauteur_maison + np.tan(np.radians(inclinaison_deg)) * (longueur_maison / 2)],
                              [longueur_maison, hauteur_maison]], color='skyblue'))

# Obstacle
x_obs = longueur_maison + distance_obstacle
color = 'green' if obstacle == "Arbre" else 'grey'
ax.add_patch(patches.Rectangle((x_obs, 0), 1, hauteur_obstacle, color=color, label=obstacle))
ax.text(x_obs, hauteur_obstacle + 0.2, f"{obstacle} ({hauteur_obstacle} m)", fontsize=9)

# Ombre
ax.add_patch(patches.Rectangle((longueur_maison, 0), longueur_ombre, 0.1, color='gray', alpha=0.4, label="Ombre"))

# Mise en page
ax.set_xlim(0, x_obs + 10)
ax.set_ylim(0, 10)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Hauteur (m)")
ax.set_title(f"Ombre projetée à {hauteur_soleil}° de hauteur solaire")
ax.grid(True)

# Affichage graphique dans Streamlit
st.pyplot(fig)

# Résumé texte
prod_loss_pct = min(100, round((longueur_ombre / 12) * 100, 1)) if longueur_ombre > 0 else 0
st.markdown(f"🌥️ **Longueur d’ombre estimée** : `{longueur_ombre:.2f} m`")
st.markdown(f"⚠️ **Taux de masquage potentiel de la toiture** : `{prod_loss_pct}%` (à vérifier avec PVsyst ou SketchUp)")
