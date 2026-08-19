import { motion } from 'framer-motion';
import './PageSkeleton.css';

export default function MeterReference() {
  return (
    <div className="page" id="meter-reference-page">
      <div className="container">
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="badge badge--indigo">Reference</span>
          <h1 className="page-header__title">Meter Encyclopedia</h1>
          <p className="page-header__subtitle">
            Browse 200+ Sanskrit meters — search by name, category, syllable
            count, or Gaṇa sequence. Each entry includes the L-G pattern,
            description, and example verse.
          </p>
        </motion.div>

        <motion.div
          className="placeholder-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="placeholder-card__icon">📚</div>
          <h2 className="placeholder-card__title">Coming in Phase 1B & 3</h2>
          <p className="placeholder-card__desc">
            The meter database (200+ entries extracted from classical sources) and
            the browsable encyclopedia UI will be available by November 2026.
          </p>
          <div className="placeholder-card__progress">
            <div className="placeholder-card__progress-bar" style={{ width: '5%' }} />
          </div>
          <span className="placeholder-card__progress-text">Data schema defined</span>
        </motion.div>
      </div>
    </div>
  );
}
