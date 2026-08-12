import { motion } from 'framer-motion';
import './PageSkeleton.css';

export default function Dashboard() {
  return (
    <div className="page" id="dashboard-page">
      <div className="container">
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="badge badge--indigo">User Dashboard</span>
          <h1 className="page-header__title">Your Analysis History</h1>
          <p className="page-header__subtitle">
            View and manage your past analyses, translations, and OCR results.
          </p>
        </motion.div>

        <motion.div
          className="placeholder-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="placeholder-card__icon">📊</div>
          <h2 className="placeholder-card__title">Coming in Phase 6</h2>
          <p className="placeholder-card__desc">
            The user system with authentication and analysis history will be
            implemented in December 2026 – January 2027.
          </p>
          <div className="placeholder-card__progress">
            <div className="placeholder-card__progress-bar" style={{ width: '5%' }} />
          </div>
          <span className="placeholder-card__progress-text">Database models defined</span>
        </motion.div>
      </div>
    </div>
  );
}
