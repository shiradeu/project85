import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';
import session from 'express-session';
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import multer from 'multer';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = 3000;

// Middleware
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}));
app.use(express.json());
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/research-db');

// File upload configuration
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname)
  }
});
const upload = multer({ storage: storage });

// Models
const Research = mongoose.model('Research', {
  userId: String,
  title: String,
  description: String,
  category: String,
  notes: String,
  file1Path: String,
  file2Path: String,
  createdAt: { type: Date, default: Date.now }
});

// // Passport configuration
// passport.use(new GoogleStrategy({
//     clientID: process.env.GOOGLE_CLIENT_ID,
//     clientSecret: process.env.GOOGLE_CLIENT_SECRET,
//     callbackURL: "http://localhost:3000/auth/google/callback"
//   },
//   function(accessToken, refreshToken, profile, cb) {
//     return cb(null, profile);
//   }
// ));

// passport.serializeUser((user, done) => {
//   done(null, user);
// });

// passport.deserializeUser((user, done) => {
//   done(null, user);
// });

// // Auth routes
// app.get('/auth/google',
//   passport.authenticate('google', { scope: ['profile', 'email'] })
// );

// app.get('/auth/google/callback', 
//   passport.authenticate('google', { failureRedirect: '/login' }),
//   function(req, res) {
//     res.redirect('http://localhost:5173');
//   }
// );

app.get('/api/user', (req, res) => {
  res.json(req.user || null);
});

// Research routes
app.post('/api/research', upload.fields([
  { name: 'file1', maxCount: 1 },
  { name: 'file2', maxCount: 1 }
]), async (req, res) => {
  try {
    const files = req.files;
    console.log( req.user);
    console.log( req.body);
    console.log( files);

    const research = new Research({
      // userId: req.user.id,
      ...req.body,
      file1Path: files?.file1?.[0]?.path,
      file2Path: files?.file2?.[0]?.path,
      userId:111
    });
    console.log( research);

    await research.save();
    res.json({ message: 'Research data saved successfully!' });
  } catch (error) {
    res.status(500).json({ error: "error.message" });
  }
});

app.get('/api/research', async (req, res) => {
  try {
   // const research = await Research.find({ userId: req.user.id })
    const research = await Research.find({ userId: 111 })
      .sort({ createdAt: -1 });
    res.json(research);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});