const mongoose = require("mongoose");

const pairingSchema = new mongoose.Schema({
  dataset1: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Dataset",
    required: true,
  },
  dataset2: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Dataset",
    required: true,
  },
  similarityScore: { type: Number, required: true },
});

const Pairing = mongoose.model("Pairing", pairingSchema);

module.exports = Pairing;
