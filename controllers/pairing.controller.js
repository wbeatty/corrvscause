const Pairing = require("../models/pairing.model");

const getPairings = async (req, res) => {
  try {
    const pairings = await Pairing.find({}).populate("dataset1 dataset2");
    res.status(200).json(pairings);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const getPairing = async (req, res) => {
  try {
    const { id } = req.params;
    const pairing = await Pairing.findById(id).populate("dataset1 dataset2");

    if (!pairing) {
      return res.status(404).json({ message: "Pairing not found" });
    }

    res.status(200).json(pairing);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const createPairing = async (req, res) => {
  try {
    const pairing = await Pairing.create(req.body);
    res.status(201).json(pairing);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const deletePairing = async (req, res) => {
  try {
    const { id } = req.params;
    const pairing = await Pairing.findByIdAndDelete(id);

    if (!pairing) {
      return res.status(404).json({ message: "Pairing not found" });
    }

    res.status(200).json({ message: "Pairing deleted successfully" });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

const getRandomPairing = async (req, res) => {
  try {
    // Check if any pairings exist first
    const count = await Pairing.countDocuments();
    if (count === 0) {
      return res.status(404).json({ message: "No pairings found in database" });
    }

    // Use MongoDB aggregation to get a random pairing
    const randomPairing = await Pairing.aggregate([
      { $sample: { size: 1 } },
      {
        $lookup: {
          from: "datasets",
          localField: "dataset1",
          foreignField: "_id",
          as: "dataset1",
        },
      },
      {
        $lookup: {
          from: "datasets",
          localField: "dataset2",
          foreignField: "_id",
          as: "dataset2",
        },
      },
      {
        $unwind: "$dataset1",
      },
      {
        $unwind: "$dataset2",
      },
    ]);

    if (!randomPairing || randomPairing.length === 0) {
      return res
        .status(404)
        .json({ message: "No random pairing could be retrieved" });
    }

    res.status(200).json(randomPairing[0]);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getPairings,
  getPairing,
  createPairing,
  deletePairing,
  getRandomPairing,
};
