import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURATION ---
FICHIE_CSV = 'Erasmus_Budget/mon_budget_erasmus.csv'
CATEGORIES = [
    "Logement & Charges",
    "Alimentation",
    "Transports",
    "Loisirs & Sorties",
    "Voyages",
    "Santé",
    "Remboursement",  # <--- Nouvelle catégorie ajoutée
    "Autre",
    "Revenus (Bourse/Salaires)"
]

# --- FONCTIONS ---

def charger_donnees():
    """Charge les données depuis le CSV ou crée un DataFrame vide si inexistant."""
    if not os.path.exists(FICHIE_CSV):
        return pd.DataFrame(columns=['Date', 'Montant', 'Catégorie', 'Description'])
    
    try:
        df = pd.read_csv(FICHIE_CSV)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return pd.DataFrame(columns=['Date', 'Montant', 'Catégorie', 'Description'])

def sauvegarder_operation(date, montant, categorie, description):
    """Ajoute une ligne au CSV."""
    nouvelle_ligne = pd.DataFrame({
        'Date': [date],
        'Montant': [montant],
        'Catégorie': [categorie],
        'Description': [description]
    })
    
    if not os.path.exists(FICHIE_CSV):
        nouvelle_ligne.to_csv(FICHIE_CSV, index=False)
    else:
        nouvelle_ligne.to_csv(FICHIE_CSV, mode='a', header=False, index=False)

def supprimer_ligne(index_a_supprimer):
    """Supprime une ligne spécifique du fichier CSV basé sur son index."""
    df = charger_donnees()
    try:
        # On supprime la ligne qui a cet index
        df = df.drop(index_a_supprimer)
        # On sauvegarde le fichier écrasé
        df.to_csv(FICHIE_CSV, index=False)
        return True
    except KeyError:
        return False

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="Mon Budget Erasmus", page_icon="💰", layout="wide")

st.title("💰 Gestion Budget Erasmus V2")

# Chargement des données
df = charger_donnees()

# Menu Latéral
menu = st.sidebar.radio(
    "Navigation", 
    ["Vue d'ensemble 📊", "Bilan Mensuel 📅", "Ajouter une opération ➕", "Gérer / Supprimer 🗑️"]
)

# --- PAGE: VUE D'ENSEMBLE ---
if menu == "Vue d'ensemble 📊":
    st.header("Vue Globale")
    
    if not df.empty:
        # KPI Globaux
        total_depenses = df[df['Montant'] < 0]['Montant'].sum()
        total_revenus = df[df['Montant'] > 0]['Montant'].sum()
        solde = total_revenus + total_depenses
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenus", f"{total_revenus:.2f} €", delta_color="normal")
        col2.metric("Total Dépenses", f"{total_depenses:.2f} €", delta_color="inverse")
        col3.metric("Solde Actuel", f"{solde:.2f} €")
        
        st.divider()

        # Graphique: Évolution du solde
        df_sorted = df.sort_values(by='Date')
        df_sorted['Solde Cumulé'] = df_sorted['Montant'].cumsum()
        
        fig_evol = px.line(df_sorted, x='Date', y='Solde Cumulé', title="Évolution de la trésorerie")
        st.plotly_chart(fig_evol, use_container_width=True)
        
    else:
        st.info("Aucune donnée disponible. Commencez par ajouter une opération.")

# --- PAGE: BILAN MENSUEL ---
elif menu == "Bilan Mensuel 📅":
    st.header("Analyse Mensuelle")
    
    if not df.empty:
        col_annee, col_mois = st.columns(2)
        
        annees = df['Date'].dt.year.unique()
        annee_sel = col_annee.selectbox("Année", sorted(annees, reverse=True))
        
        # Filtrer les mois disponibles pour l'année sélectionnée
        df_annee = df[df['Date'].dt.year == annee_sel]
        mois_dispos = df_annee['Date'].dt.month_name().unique()
        mois_sel = col_mois.selectbox("Mois", mois_dispos)
        
        # Filtrage final
        mask = (df['Date'].dt.year == annee_sel) & (df['Date'].dt.month_name() == mois_sel)
        df_filtered = df[mask]
        
        # Séparation Dépenses / Revenus pour graphiques
        df_depenses = df_filtered[df_filtered['Montant'] < 0].copy()
        df_depenses['Montant_Positif'] = df_depenses['Montant'].abs()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Répartition")
            st.metric("Dépenses du mois", f"{df_depenses['Montant'].sum():.2f} €")
            if not df_depenses.empty:
                fig_pie = px.pie(df_depenses, values='Montant_Positif', names='Catégorie', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.write("Pas de dépenses ce mois-ci.")
                
        with col2:
            st.subheader("Détail des opérations")
            st.dataframe(df_filtered.sort_values(by='Date', ascending=False), use_container_width=True)

    else:
        st.info("Ajoutez des données pour voir le bilan mensuel.")

# --- PAGE: AJOUTER OPERATION ---
elif menu == "Ajouter une opération ➕":
    st.header("Nouvelle Transaction")
    
    with st.form("ajout_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date_op = col1.date_input("Date", datetime.today())
        montant = col2.number_input("Montant (€) - (Négatif=Dépense, Positif=Revenu)", step=0.01, format="%.2f")
        
        categorie = st.selectbox("Catégorie", CATEGORIES)
        description = st.text_input("Description (ex: Lidl, Loyer, Bar...)")
        
        submit = st.form_submit_button("Enregistrer")
        
        if submit:
            if montant == 0:
                st.warning("Le montant ne peut pas être nul.")
            else:
                sauvegarder_operation(date_op, montant, categorie, description)
                st.success("Opération enregistrée avec succès !")
                st.rerun()

# --- PAGE: GÉRER / SUPPRIMER ---
elif menu == "Gérer / Supprimer 🗑️":
    st.header("Historique et Suppression")
    
    if not df.empty:
        st.write("Cochez le numéro (Index) de la ligne à gauche pour identifier celle à supprimer.")
        
        # On affiche le tableau complet
        # On trie par date décroissante pour voir les derniers ajouts en premier
        df_display = df.sort_values(by='Date', ascending=False)
        st.dataframe(df_display, use_container_width=True)
        
        st.divider()
        st.subheader("Supprimer une ligne")
        
        # Sélecteur pour choisir l'ID à supprimer
        # On récupère tous les index disponibles
        liste_index = df_display.index.tolist()
        
        col_del1, col_del2 = st.columns([3, 1])
        index_to_delete = col_del1.selectbox("Sélectionnez le numéro (Index) de la ligne à supprimer :", liste_index)
        
        if col_del2.button("🗑️ Supprimer"):
            success = supprimer_ligne(index_to_delete)
            if success:
                st.success(f"Ligne n°{index_to_delete} supprimée avec succès !")
                st.rerun()
            else:
                st.error("Erreur lors de la suppression.")
    else:
        st.info("Aucune opération à gérer.")