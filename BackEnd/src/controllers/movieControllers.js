// controller/movieController.js
const Movie = require("../models/movie");

const saveMovieData = async (req, res) => {
  try {
    const { username, ...movieData } = req.body;

    // Ensure username is present
    if (!username) {
      return res.status(400).json({ error: "Username is required." });
    }

    const movie = new Movie({ username, ...movieData });
    await movie.save();
    res.status(201).json({ message: "Movie data saved successfully!" });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Fetch history by username
const getUserHistory = async (req, res) => {
  try {
    const { username } = req.params;

    // Find movies associated with the username
    const movies = await Movie.find({ username });
    res.status(200).json(movies);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = { saveMovieData, getUserHistory };
