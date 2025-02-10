import { MongoClient } from 'mongodb';

const uri = "mongodb://localhost:27017";
const client = new MongoClient(uri);

async function run() {
    try {
        await client.connect();
        console.log("Connected to MongoDB!");
        const db = client.db("test");

        // Access the 'users' collection (you can change this to any collection)
        const collection = db.collection("users");

        // Define the document to insert
        const newUser = {
            name: "John Doe",
            age: 30,
            email: "johndoe@example.com",
            createdAt: new Date()
        };

        // Insert the document into the collection
        const result = await collection.insertOne(newUser);
        console.log(`New user inserted with ID: ${result.insertedId}`);

        // Perform database operations...
    } finally {
        await client.close();
    }
}

run().catch(console.dir);
