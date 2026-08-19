import { motion } from 'framer-motion';
import './PageSkeleton.css';

export default function OcrPage() {
  return (
    <div className="page" id="ocr-page">
      <div className="container">
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="badge badge--saffron">Smart OCR</span>
          <h1 className="page-header__title">Image Text Extraction</h1>
          <p className="page-header__subtitle">
            Upload images of Sanskrit manuscripts or printed text. Extract text
            with Gemini Vision + Tesseract OCR, enhanced by meter-aware error
            correction.
          </p>
        </motion.div>

        <motion.div
          className="placeholder-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="placeholder-card__icon">📸</div>
          <h2 className="placeholder-card__title">Coming in Phase 5</h2>
          <p className="placeholder-card__desc">
            The OCR pipeline with meter-aware correction will be implemented in
            December 2026, featuring dual OCR (Gemini Vision + Tesseract) and
            intelligent post-processing using prosodic pattern matching.
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
