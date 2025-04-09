import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configuration des styles
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (8, 3)
plt.rcParams['font.size'] = 9
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Données complètes
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
data = {
    # Économie réelle
    'PIB réel': [2.9, -7.2, 8.2, 1.5, 3.4, 2.9, 4, 3.6],
    'PIB agricole': [-5, -8.1, 19.5, -11.3, 1.4, -3.3, 9.5, 0.7],
    'PIB non agricole': [3.8, -7.1, 8.9, 3.2, 3.8, 3.7, 3.8, 4],
    'Industrie': [4.1, -5.2, 7.8, -2.7, 1.3, 3, 3.2, 3.3],
    'Services': [3.9, -7.9, 5.7, 8.8, 4.4, 3.7, 3.5, 4.2],
    
    # Demande
    'Consommation privée': [2.2, -5.8, 6.8, 0, 3.7, 4, 4.2, 3.7],
    'Consommation publique': [4.6, -6.6, 7.2, 3, 4.1, 4.6, 4.1, 3.6],
    'Investissement fixe': [1.7, -10, 7.5, -4, 1.9, 3.9, 4.3, 4.5],
    
    # Commerce extérieur
    'Exportations': [5.1, -15, 7.9, 20.5, 8.8, 7.6, 8.3, 8.1],
    'Importations': [2.1, -11.9, 10.4, 9.5, 7.4, 8.2, 6.3, 7],
    
    # Emploi & Prix
    'Taux de chômage (OIT)': [9.2, 11.9, 12.3, 11.8, 13, np.nan, np.nan, np.nan],
    'Inflation (IPC)': [0.2, 0.7, 1.4, 6.6, 6.1, 1.5, 2.7, 2.4],
    
    # Finances publiques
    'Dépenses publiques (% PIB)': [27.4, 34.1, 31.3, 34.1, 33, 33.1, 30.8, 29.5],
    'Recettes publiques (% PIB)': [23.8, 27.7, 25.8, 28.7, 28.8, 28.8, 27, 26.3],
    'Déficit public (% PIB)': [-3.6, -7.1, -5.5, -5.4, -4.3, -4.4, -3.8, -3.3],
    'Dette publique (% PIB)': [60.3, 72.2, 69.4, 71.5, 69.5, 70, 66.6, 67.2],
    
    # Balance des paiements
    'Compte courant (% PIB)': [-3.4, -1.2, -2.3, -3.8, -0.6, -1.5, -2.8, -2.8],
    'IDE net (% PIB)': [0.6, 0.8, 1.1, 1.2, 0.2, 1, 1.1, 1.2],
    'Réserves de change (mois d\'import)': [6.9, 7.1, 5.3, 5.4, 5.5, 5.3, 5.4, 5.6],
    
    # Macro
    'PIB nominal (Md$)': [1240, 1152, 1277, 1331, 1463, 1529, 1653, 1732]
}

# Initialisation Streamlit
st.set_page_config(layout="wide", page_title="Indicateurs Économiques Maroc")
st.title("📊 Tableau de Bord Économique du Maroc (2019-2026)")
st.caption("Source : Rapport de suivi de la situation économique au Maroc - Banque mondiale, MEC, HCP et BAM")


# Section 1: Affichage du tableau complet
st.header("📋 Tableau Complet des Indicateurs")
df = pd.DataFrame(data, index=years).transpose()
st.dataframe(df.style.format("{:.1f}", na_rep="-"), height=800, use_container_width=True)
st.markdown("---")

# Section 2: Graphiques individuels
st.header("📈 Visualisation par Indicateur")

# Fonction de création de graphique
def create_single_plot(indicator, unit):
    fig, ax = plt.subplots()
    
    clean_years = [year for year, val in zip(years, data[indicator]) if not np.isnan(val)]
    clean_values = [val for val in data[indicator] if not np.isnan(val)]
    
    ax.plot(clean_years, clean_values, 
            color=colors[0],
            marker='o',
            markersize=5,
            linewidth=2,
            markerfacecolor='white')
    
    ax.set_title(indicator, pad=10, fontsize=11, fontweight='bold')
    ax.set_ylabel(unit, fontsize=9)
    ax.grid(alpha=0.2)
    plt.xticks(clean_years, rotation=45)
    plt.tight_layout()
    return fig

# Organisation des graphiques par catégories
categories = {
    "Économie Réelle": ['PIB réel', 'PIB agricole', 'PIB non agricole', 'Industrie', 'Services'],
    "Demande": ['Consommation privée', 'Consommation publique', 'Investissement fixe'],
    "Commerce Extérieur": ['Exportations', 'Importations'],
    "Marché du Travail & Prix": ['Taux de chômage (OIT)', 'Inflation (IPC)'],
    "Finances Publiques": ['Dépenses publiques (% PIB)', 'Recettes publiques (% PIB)', 
                         'Déficit public (% PIB)', 'Dette publique (% PIB)'],
    "Balance des Paiements": ['Compte courant (% PIB)', 'IDE net (% PIB)', 
                             'Réserves de change (mois d\'import)'],
    "Indicateurs Macro": ['PIB nominal (Md$)']
}

# Génération des graphiques
for category, indicators in categories.items():
    st.subheader(f"🔹 {category}")
    cols = st.columns(2)
    
    for idx, indicator in enumerate(indicators):
        with cols[idx % 2]:
            unit = "%" if "PIB" in indicator or "%" in indicator else "Milliards USD" if "Md$" in indicator else "Mois" if "import" in indicator else "%"
            fig = create_single_plot(indicator, unit)
            st.pyplot(fig, use_container_width=True)
    
    st.markdown("---")

# Style CSS
st.markdown("""
<style>
    [data-testid=stSidebar], .stDeployButton, footer, #MainMenu, header {visibility: hidden;}
    .stPlot {border: 1px solid #f0f2f6; border-radius: 8px; padding: 15px;}
    .stMarkdown > hr {margin: 0.8rem 0 !important;}
    h2, h3 {color: #2a3f5f;}
    .stDataFrame {font-size: 0.9em;}
</style>
""", unsafe_allow_html=True)