import { motion } from 'framer-motion';
import './About.css';

const techStack = [
  { category: 'Frontend', items: ['React 18', 'Vite 5', 'Framer Motion', 'React Router v6'] },
  { category: 'Backend', items: ['Python 3.11', 'Flask 3.x', 'SQLAlchemy', 'Gunicorn'] },
  { category: 'NLP Engine', items: ['Custom Syllable Parser', 'Laghu-Guru Classifier', 'Sandhi Splitter', 'LSTM Classifier'] },
  { category: 'AI & OCR', items: ['Google Gemini API', 'Groq API', 'Tesseract 5', 'OpenCV'] },
  { category: 'Database', items: ['PostgreSQL (Render)', 'SQLite (dev)'] },
  { category: 'Deployment', items: ['Render (Backend)', 'Vercel (Frontend)', 'UptimeRobot'] },
];

const disciplines = [
  'Computational Linguistics',
  'Machine Learning',
  'Computer Vision',
  'Natural Language Processing',
  'Full-Stack Engineering',
  'Research Methodology',
];

export default function About() {
  return (
    <div className="page about" id="about-page">
      <div className="container container--narrow">
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="badge badge--indigo">About</span>
          <h1 className="page-header__title">About Chandas</h1>
          <p className="page-header__subtitle">
            A comprehensive Sanskrit prosody analysis platform — Final Year
            College Project
          </p>
        </motion.div>

        <motion.section
          className="about__section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h2>What is Chandas?</h2>
          <p>
            <strong>Chandas</strong> (छन्दस्) refers to the system of poetic meters
            in Sanskrit literature. Originating with Piṅgala's <em>Chandaḥśāstra</em>,
            this ancient classification system governs the rhythmic structure of Sanskrit
            verse through patterns of light (Laghu) and heavy (Guru) syllables.
          </p>
          <p>
            This project brings classical Sanskrit prosody into the digital age with a
            <strong> custom-built analysis engine</strong> capable of identifying 200+
            meters, performing sandhi analysis, providing word-by-word translations, and
            extracting text from manuscript images.
          </p>
        </motion.section>

        <motion.section
          className="about__section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2>Technical Disciplines</h2>
          <div className="about__disciplines">
            {disciplines.map((d, i) => (
              <span key={i} className="badge badge--indigo about__discipline-badge">
                {d}
              </span>
            ))}
          </div>
        </motion.section>

        <motion.section
          className="about__section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <h2>Technology Stack</h2>
          <div className="about__tech-grid">
            {techStack.map((group, i) => (
              <div key={i} className="about__tech-card card">
                <h3>{group.category}</h3>
                <ul>
                  {group.items.map((item, j) => (
                    <li key={j}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </motion.section>

        <motion.section
          className="about__section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h2>Key Differentiators</h2>
          <ul className="about__features-list">
            <li>
              <strong>Custom-built engine</strong> — Not a library wrapper. All syllable
              parsing, L-G classification, and pattern matching built from scratch.
            </li>
            <li>
              <strong>Sandhi analysis</strong> — Rule-based splitter covering 45+ sandhi
              rules across vowel, consonant, and visarga types.
            </li>
            <li>
              <strong>Padaccheda translation</strong> — Word-by-word grammatical analysis
              alongside natural translations.
            </li>
            <li>
              <strong>Meter-aware OCR correction</strong> — Novel combination of prosody
              and computer vision for intelligent error correction.
            </li>
            <li>
              <strong>3-tier hybrid architecture</strong> — Exact match → Fuzzy search →
              LSTM classifier for robust identification.
            </li>
          </ul>
        </motion.section>
      </div>
    </div>
  );
}
