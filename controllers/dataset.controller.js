const Dataset = require("../models/dataset.model");

const getDatasets = async (req, res) => {
  try {
    const datasets = await Dataset.find({});
    res.status(200).json(datasets);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const getDataset = async (req, res) => {
  try {
    const { id } = req.params;
    const dataset = await Dataset.findById(id);
    res.status(200).json(dataset);
  } catch (error) {
    res;
  }
};

const createDataset = async (req, res) => {
  try {
    const dataset = await Dataset.create(req.body);
    res.status(201).json(dataset);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const updateDataset = async (req, res) => {
  try {
    const { id } = req.params;
    const dataset = await Dataset.findByIdAndUpdate(id, req.body);

    if (!dataset) {
      return res.status(404).json({ message: "Dataset not found" });
    }

    const updatedProduct = await Dataset.findById(id);
    res.status(200).json(updatedProduct);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const deleteDataset = async (req, res) => {
  try {
    const { id } = req.params;
    const dataset = await Dataset.findByIdAndDelete(id);

    if (!dataset) {
      return res.status(404).json({ message: "Dataset not found" });
    }

    res.status(200).json({ message: "Dataset deleted successfully" });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getDatasets,
  getDataset,
  createDataset,
  updateDataset,
  deleteDataset,
};
