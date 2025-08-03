const mongoose = require("mongoose");

const datasetSchema = new mongoose.Schema({
  id: { type: String, required: true },
  name: { type: String, required: true },
  years: [Number],
  values: [Number],
});

const Dataset = mongoose.model("Dataset", datasetSchema);

module.exports = Dataset;
