import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer" id="main-footer">
      <div className="container">
        <div className="footer__inner">
          {/* Brand */}
          <div className="footer__brand">
            <Link to="/" className="footer__logo">
              <span className="footer__logo-icon">छ</span>
              <span className="footer__logo-text">Chandas</span>
            </Link>
            <p className="footer__tagline">
              Identifying Sanskrit Poetic Meters with AI
            </p>
          </div>

          {/* Links */}
          <div className="footer__links">
            <div className="footer__col">
              <h4 className="footer__col-title">Tools</h4>
              <Link to="/analyzer" className="footer__link">Chandas Analyzer</Link>
              <Link to="/translator" className="footer__link">Sanskrit Translator</Link>
              <Link to="/ocr" className="footer__link">Image OCR</Link>
            </div>
            <div className="footer__col">
              <h4 className="footer__col-title">Resources</h4>
              <Link to="/meters" className="footer__link">Meter Encyclopedia</Link>
              <Link to="/about" className="footer__link">About</Link>
            </div>
          </div>
        </div>

        <div className="footer__bottom">
          <p className="footer__copyright">
            © {new Date().getFullYear()} Chandas Project — Final Year Project
          </p>
          <p className="footer__sanskrit devanagari">
            छन्दांसि जगतां पदवीम् — Meters are the footsteps of the universe
          </p>
        </div>
      </div>
    </footer>
  );
}
