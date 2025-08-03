const express = require("express");
const Dataset = require("../models/dataset.model");
const router = express.Router();
const {
  getDatasets,
  getDataset,
  createDataset,
  updateDataset,
  deleteDataset,
} = require("../controllers/dataset.controller");

router.get("/", getDatasets);

router.get("/:id", getDataset);

router.post("/", createDataset);

router.put("/:id", updateDataset);

router.delete("/:id", deleteDataset);

module.exports = router;
