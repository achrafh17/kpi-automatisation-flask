import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from kpi_processor import KPIProcessor

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")
# Autorise les requêtes du frontend React
# Dossier pour stocker les fichiers uploadés
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuration des seuils ISO
ISO_THRESHOLDS = {
   
    'Taux_de_livraison_à_temps': {'min': 0.90, 'max': 1.00},
    'Coût_de_transport_par_unité': {'min': 0.00, 'max': 5.00},
    'Taux de remplissage des véhicules': {'min': 0.70, 'max': 1.00},
    'Kilomètres à vide': {'min': 0.00, 'max': 0.20},  # Par exemple, un ratio maximum de 20%
    'Taux de rotation des stocks': {'min': 2.0, 'max': 10.0},  # Nombre de fois que le stock se renouvelle
    'Taux_d_occupation_de_l_entrepôt': {'min': 0.50, 'max': 0.90},  # Entre 50% et 90% d'occupation
    'Productivité picking': {'min': 20.0, 'max': 60.0},  # Nombre de lignes préparées par heure, par exemple
    'Précision des stocks': {'min': 0.95, 'max': 1.00},
    'Taux de satisfaction client': {'min': 0.90, 'max': 1.00},
    'Taux de réclamations': {'min': 0.00, 'max': 0.05},  # Maximum 5% de réclamations
    'Perfect Order Rate': {'min': 0.90, 'max': 1.00},
    'Taux de casse': {'min': 0.00, 'max': 0.02},  # Maximum 2% de casse
    'Taux d erreurs de préparation': {'min': 0.00, 'max': 0.03},  # Maximum 3% d'erreurs
    'Marge opérationnelle': {'min': 0.05, 'max': 0.30},  # Entre 5% et 30%
    'Coût par commande': {'min': 0.00, 'max': 50.00}         # ratio
}

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Début de la fonction upload_file")
    print("hello")

    # Vérifier que le fichier est bien dans la requête
    if 'file' not in request.files:
        print("Erreur : Aucun fichier dans la requête")
        return jsonify({'error': 'Aucun fichier'}), 400

    file = request.files['file']
    print("Nom du fichier:", file.filename)

    if file.filename == '':
        print("Erreur : Nom de fichier vide")
        return jsonify({'error': 'Fichier vide'}), 400

    # Sauvegarde du fichier
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        print("Chemin de sauvegarde:", file_path)
        file.save(file_path)
        print("Fichier sauvegardé avec succès")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        return jsonify({'error': str(e)}), 500

    # Traitement du fichier CSV pour calculer et valider les KPIs
    processor = KPIProcessor(ISO_THRESHOLDS)
    try:
        df = processor.load_csv(file_path)
        kpis = processor.calculate_kpis(df)
        validation = processor.validate_kpis(kpis)
        return jsonify({
            'message': 'Fichier téléchargé avec succès',
            'kpis': kpis,
       
            'validation': validation
        }), 200
    except Exception as e:
        print(f"Erreur lors du traitement du CSV : {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
