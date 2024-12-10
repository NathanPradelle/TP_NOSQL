from pymongo import MongoClient
import matplotlib.pyplot as plt

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["reunion"]
collection = db["tourisme"]

def aggregate_and_plot(field, title, xlabel, ylabel, output_file):
    # Agrégation MongoDB
    pipeline = [
        {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    results = list(collection.aggregate(pipeline))
    
    # Préparer les données pour l'histogramme
    labels = [r["_id"] if r["_id"] is not None else "Inconnu" for r in results]
    values = [r["count"] for r in results]
    
    # Générer l'histogramme
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()

# 1. Hébergements par type
aggregate_and_plot(
    field="type_hebergement",
    title="Nombre d'hébergements par type",
    xlabel="Type d'hébergement",
    ylabel="Nombre",
    output_file="hebergements_par_type.png"
)

# 2. Hébergements par zone touristique
aggregate_and_plot(
    field="zone_touristique",
    title="Nombre d'hébergements par zone touristique",
    xlabel="Zone touristique",
    ylabel="Nombre",
    output_file="hebergements_par_zone.png"
)

# 3. Hébergements par classement
aggregate_and_plot(
    field="classement",
    title="Nombre d'hébergements par classement",
    xlabel="Classement",
    ylabel="Nombre",
    output_file="hebergements_par_classement.png"
)

# 4. Hébergements par mode de paiement
pipeline = [
    {"$unwind": "$modes_paiement"},  # Décompose le tableau des modes de paiement
    {"$group": {"_id": "$modes_paiement", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = list(collection.aggregate(pipeline))

# Préparer les données pour l'histogramme
labels = [r["_id"] for r in results]
values = [r["count"] for r in results]

# Générer un histogramme pour les modes de paiement
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color='orange')
plt.title("Nombre d'hébergements par mode de paiement")
plt.xlabel("Mode de paiement")
plt.ylabel("Nombre")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("hebergements_par_mode_paiement.png")
plt.show()
