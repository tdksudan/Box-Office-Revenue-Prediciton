// models/Movie.js
const mongoose = require("mongoose");

const MovieSchema = new mongoose.Schema({
  username: { type: String, required: true }, // Reference to the user
  budget: { type: Number, required: true },
  runtime: { type: Number, required: true },
  release_date: { type: Date, required: true },
  votes: { type: Number, required: true },
  score: { type: Number, required: true },
  name: { type: String, required: true },
  rating: { type: String, required: true },
  genre: { type: String, required: true },
  director: { type: String, required: true },
  writer: { type: String, required: true },
  star: { type: String, required: true },
  company: { type: String, required: true },
  country: { type: String, required: true },
  box_office_revenue: { type: Number, required: true },
});

module.exports = mongoose.model("Movie", MovieSchema);
