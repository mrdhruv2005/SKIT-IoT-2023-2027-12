import { motion } from 'framer-motion';
import './PageSkeleton.css';

export default function ChandasAnalyzer() {
  return (
    <div className="page" id="chandas-analyzer-page">
      <div className="container">
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="badge badge--saffron">Core Feature</span>
          <h1 className="page-header__title">Chandas Analyzer</h1>
          <p className="page-header__subtitle">
            Enter Sanskrit text to identify its poetic meter, view syllable
            breakdown, Laghu-Guru patterns, Gaṇa notation, and Sandhi analysis.
          </p>
        </motion.div>

        <motion.div
          className="placeholder-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="placeholder-card__icon">🔍</div>
          <h2 className="placeholder-card__title">Coming in Phase 1 & 3</h2>
          <p className="placeholder-card__desc">
            The Chandas analysis engine is being built from scratch — including
            custom syllable parsing, Laghu-Guru classification, and pattern
            matching. The full analyzer UI will be available by November 2026.
          </p>
          <div className="placeholder-card__progress">
            <div className="placeholder-card__progress-bar" style={{ width: '15%' }} />
          </div>
          <span className="placeholder-card__progress-text">Phase 0 complete — foundation laid</span>
        </motion.div>
      </div>
    </div>
  );
}
