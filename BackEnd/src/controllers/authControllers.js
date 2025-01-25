const { COOKIE_SECRET } = require('../config/config');
const bcrypt = require('bcryptjs');  //  for hashing passwords
const User = require('../models/user'); // storage for users (as  database is used)

// Registration
exports.registerUser = async (req, res) => {
    const { username, email, password } = req.body;
  
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'All fields are required' });
    }
  
    try {
      const existingUser = await User.findOne({ username });
      if (existingUser) {
        return res.status(400).json({ error: 'Username already exists' });
      }
  
      // Hash password before saving
      const hashedPassword = await bcrypt.hash(password, 10);
  
      const newUser = new User({ username, email, password: hashedPassword });
      await newUser.save();
  
      return res.status(201).json({ message: 'User registered successfully' });
    } catch (err) {
      return res.status(500).json({ error: 'Server error' });
    }
  };

// Login
exports.loginUser = async (req, res) => {
    const { username, password } = req.body;
  
    if (!username || !password) {
      return res.status(400).json({ error: 'Both username and password are required' });
    }
  
    try {
      const user = await User.findOne({ username });
      if (!user) {
        return res.status(401).json({ error: 'Invalid username or password' });
      }
  
      // Compare the hashed password
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res.status(401).json({ error: 'Invalid username or password' });
      }
  
      const token = Buffer.from(`${username}:${COOKIE_SECRET}`).toString('base64');
      res.cookie('authToken', token, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 });
  
      return res.status(200).json({ message: 'Login successful' });
    } catch (err) {
      return res.status(500).json({ error: 'Server error' });
    }
  };

// Logout
exports.logoutUser = (req, res) => {
    res.clearCookie('authToken');
    return res.status(200).json({ message: 'Logout successful' });
};