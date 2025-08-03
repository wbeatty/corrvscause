const express = require("express");
const Pairing = require("../models/pairing.model");
const router = express.Router();
const {
  getPairings,
  getPairing,
  createPairing,
  deletePairing,
  getRandomPairing,
} = require("../controllers/pairing.controller");

router.get("/", getPairings);

// IMPORTANT: Put /random BEFORE /:id to avoid conflicts
router.get("/random", getRandomPairing);

router.get("/:id", getPairing);

router.post("/", createPairing);

router.delete("/:id", deletePairing);

module.exports = router;
