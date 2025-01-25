// routes/movieRoutes.js
const express = require("express");
const { saveMovieData, getUserHistory } = require("../controllers/movieControllers");

const router = express.Router();

// Route to save movie data
router.post("/savemovie", saveMovieData);

// Route to get user history
router.get("/history/:username", getUserHistory);

module.exports = router;
