import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './Toast.css';

export default function Toast({ message, type = 'info', duration = 4000, onClose }) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(onClose, 300);
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const icons = {
    success: '✓',
    error: '✗',
    warning: '⚠',
    info: 'ℹ',
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className={`toast toast--${type}`}
          initial={{ opacity: 0, y: 40, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 40, scale: 0.95 }}
          transition={{ type: 'spring', stiffness: 400, damping: 25 }}
          id="toast-notification"
        >
          <span className="toast__icon">{icons[type]}</span>
          <span className="toast__message">{message}</span>
          <button
            className="toast__close"
            onClick={() => {
              setVisible(false);
              setTimeout(onClose, 300);
            }}
            aria-label="Close notification"
          >
            ×
          </button>
          <motion.div
            className="toast__progress"
            initial={{ scaleX: 1 }}
            animate={{ scaleX: 0 }}
            transition={{ duration: duration / 1000, ease: 'linear' }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
