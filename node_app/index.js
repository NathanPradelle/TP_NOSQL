const axios = require("axios");
const { MongoClient } = require("mongodb");

// Configuration MongoDB
const MONGO_URI = "mongodb://localhost:27017";
const DB_NAME = "reunion";
const COLLECTION_TOURISME = "tourisme";
const COLLECTION_LIEUX = "lieux";

// Fonction pour connecter à MongoDB
async function connectToMongo() {
    const client = new MongoClient(MONGO_URI);
    await client.connect();
    console.log("Connecté à MongoDB");
    return client.db(DB_NAME);
}

// Fonction pour récupérer les données paginées
async function fetchData(apiUrl) {
    let allData = [];
    let page = 1;
    const rowsPerPage = 100; // Nombre de résultats par page

    while (true) {
        const url = `${apiUrl}?start=${(page - 1) * rowsPerPage}&rows=${rowsPerPage}`;
        console.log(`Fetching: ${url}`);

        const response = await axios.get(url);
        const data = response.data.records;

        if (!data || data.length === 0) break; // Arrêter si aucune donnée restante

        allData = allData.concat(data);
        page++;
    }

    console.log(`Fetched ${allData.length} records from ${apiUrl}`);
    return allData;
}

// Fonction pour insérer les données dans MongoDB
async function insertData(collectionName, data, db) {
    const collection = db.collection(collectionName);
    await collection.insertMany(data);
    console.log(`Inserted ${data.length} records into ${collectionName}`);
}

(async () => {
    const db = await connectToMongo();

    // URL des APIs
    const API_TOURISME = "https://data.regionreunion.com/explore/dataset/etablissements-touristiques-lareunionwssoubik/table";
    const API_LIEUX = "https://data.regionreunion.com/api/records/1.0/search/?dataset=lieux-remarquableslareunion-wssoubik/table";

    // Récupérer et insérer les données des établissements touristiques
    const tourismeData = await fetchData(API_TOURISME);
    await insertData(COLLECTION_TOURISME, tourismeData, db);

    // Récupérer et insérer les données des lieux remarquables
    const lieuxData = await fetchData(API_LIEUX);
    await insertData(COLLECTION_LIEUX, lieuxData, db);

    console.log("Toutes les données ont été insérées avec succès !");
    process.exit(0); // Terminer le processus
})();