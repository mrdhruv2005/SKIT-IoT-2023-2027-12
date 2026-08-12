import { motion } from 'framer-motion';
import './PageSkeleton.css';

export default function Translator() {
  return (
    <div className="page" id="translator-page">
      <div className="container">
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="badge badge--saffron">AI-Powered</span>
          <h1 className="page-header__title">Sanskrit Translator</h1>
          <p className="page-header__subtitle">
            Translate Sanskrit to Hindi and English with detailed Padaccheda —
            word-by-word grammatical analysis and sandhi splitting.
          </p>
        </motion.div>

        <motion.div
          className="placeholder-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="placeholder-card__icon">🔤</div>
          <h2 className="placeholder-card__title">Coming in Phase 4</h2>
          <p className="placeholder-card__desc">
            The translation module with Padaccheda (word-by-word analysis) will be
            implemented in November–December 2026, featuring Gemini and Groq API
            integration with structured prompt engineering.
          </p>
          <div className="placeholder-card__progress">
            <div className="placeholder-card__progress-bar" style={{ width: '5%' }} />
          </div>
          <span className="placeholder-card__progress-text">API endpoints defined</span>
        </motion.div>
      </div>
    </div>
  );
}
