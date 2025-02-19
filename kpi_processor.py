import pandas as pd
from datetime import datetime
class KPIProcessor:
    def __init__(self, iso_thresholds):
        self.iso_thresholds = iso_thresholds

    def load_csv(self, file_path):
        """
        Charge le fichier CSV et vérifie que les colonnes nécessaires sont présentes.
        Colonnes attendues : 'delivery_time', 'transport_cost', 'load_factor'
        """
        
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        required_columns = ['Date', 'Entrepôt', 'Kilomètres_à_vide', 'Capacité_total_km_parcourus',
                            'Stock_moyen','Sorties_annuelles', 'Surface_occupée', 'Surface_totale',
                            'Lignes_préparées','Heures_travaillées', 'Stock_physique','Stock_théorique',
                            'Clients_satisfaits','Total_clients_interrogés','Nombre_de_réclamations',
                            'Total_commandes','Commandes_parfaites', 'Valeur_marchandises_endommagées','Nombre_de_livraisons_à_temps',
                            'Nombre_total_de_livraisons','Coût_total_transport', 'Nombre_unités_transportées',
                            'Volume_utilisé','Capacité_totale', 'Erreurs_de_picking', 'Total_lignes_préparées',
                            'Coûts_totaux', 'Résultat_opérationnel', 'Chiffre_d_affaires']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Colonne manquante : {col}")
        return df

    def calculate_kpis(self, df):
        """
        Calcule les KPIs principaux (moyennes) et convertit le résultat en types Python.
        """
        kpis = {
            'date': df['Date'].dt.strftime('%Y-%m-%d').iloc[0],
            'Taux_de_livraison_à_temps': float(df['Nombre_de_livraisons_à_temps'].mean()/df['Nombre_total_de_livraisons'].mean()),
            'Coût_de_transport_par_unité': float(df['Coût_total_transport'].mean()/df['Nombre_unités_transportées'].mean()),
            'Taux de remplissage des véhicules': float(df['Volume_utilisé'].mean()/df['Capacité_totale'].mean()),
            'Kilomètres à vide': float(df['Kilomètres_à_vide'].mean()/df['Capacité_total_km_parcourus'].mean()),
            'Taux de rotation des stocks': float(df['Sorties_annuelles'].mean()/df['Stock_moyen'].mean()),
            'Taux_d_occupation_de_l_entrepôt': float(df['Surface_occupée'].mean()/df['Surface_totale'].mean()),
            'Productivité picking': float(df['Lignes_préparées'].mean()/df['Heures_travaillées'].mean()),
            'Précision des stocks': float(df['Stock_physique'].mean()/df['Stock_théorique'].mean()),
            'Taux de satisfaction client': float(df['Clients_satisfaits'].mean()/df['Total_clients_interrogés'].mean()),
            'Taux de réclamations': float(df['Nombre_de_réclamations'].mean()/df['Total_commandes'].mean()),
            'Perfect Order Rate': float(df['Commandes_parfaites'].mean()/df['Total_commandes'].mean()),
            'Taux de casse': float(df['Valeur_marchandises_endommagées'].mean()/df['Chiffre_d_affaires'].mean()),
            'Taux d erreurs de préparation': float(df['Erreurs_de_picking'].mean()/df['Total_lignes_préparées'].mean()),
            'Marge opérationnelle': float(df['Résultat_opérationnel'].mean()/df['Chiffre_d_affaires'].mean()),
            'Coût par commande': float(df['Coûts_totaux'].mean()/df['Total_commandes'].mean()),
        
        }
        return kpis

    def validate_kpis(self, kpis):
        """
        Valide chaque KPI en vérifiant s'il est compris dans les seuils ISO définis.
        Convertit également les résultats en types Python natifs.
        """
        results = {}
        for kpi, value in kpis.items():
            if kpi in self.iso_thresholds and kpi != 'date':
                threshold = self.iso_thresholds[kpi]
                # La comparaison peut renvoyer un numpy.bool_, on le convertit en bool
                compliant = bool(threshold['min'] <= value <= threshold['max'])
                results[kpi] = {
                    'value': float(value),
                    'iso_compliant': compliant,
                    'status': 'Conforme' if compliant else 'Non Conforme'
                }
        return results
