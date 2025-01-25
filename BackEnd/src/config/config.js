require('dotenv').config();

module.exports = {
  COOKIE_SECRET: process.env.COOKIE_SECRET ,
  MONGODB_URI: process.env.MONGODB_URI ,
};
