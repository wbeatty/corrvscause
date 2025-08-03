const express = require("express");
const mongoose = require("mongoose");
const Dataset = require("./models/dataset.model");
const datasetRoute = require("./routes/dataset.route");
const pairingRoute = require("./routes/pairing.route");
const app = express();

app.use(express.json());
require("dotenv").config({ path: ".env" });
app.use(express.static("./static"));

mongoose
  .connect(process.env.DATABASE)
  .then(() => {
    console.log("Connected to MongoDB");
    app.listen(3000, () => {
      console.log("Server is running on http://localhost:3000");
    });
  })
  .catch(() => {
    console.log("Failed to connect to MongoDB");
  });

// routes
app.use("/api/datasets", datasetRoute);
app.use("/api/pairings", pairingRoute);

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});
