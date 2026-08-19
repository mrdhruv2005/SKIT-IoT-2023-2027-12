import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Home.css';

const features = [
  {
    icon: '🔍',
    title: 'Chandas Identification',
    desc: 'Identify Sanskrit poetic meters (Chandas) with our custom-built engine supporting 200+ meters, Laghu-Guru analysis, and Gaṇa notation.',
    link: '/analyzer',
    badge: 'Core Feature',
  },
  {
    icon: '🔤',
    title: 'Sanskrit Translator',
    desc: 'Translate Sanskrit to Hindi and English with detailed Padaccheda — word-by-word grammatical analysis.',
    link: '/translator',
    badge: 'AI-Powered',
  },
  {
    icon: '📸',
    title: 'Image OCR',
    desc: 'Extract Sanskrit text from images with dual OCR (Gemini Vision + Tesseract) and meter-aware correction.',
    link: '/ocr',
    badge: 'Smart OCR',
  },
  {
    icon: '📖',
    title: 'Sandhi Analysis',
    desc: 'Rule-based Sandhi splitter covering vowel, consonant, and visarga sandhi for accurate word-level analysis.',
    link: '/analyzer',
    badge: 'NLP',
  },
  {
    icon: '🧠',
    title: 'LSTM Fallback',
    desc: 'Deep learning classifier trained on 5000+ labeled verses acts as an intelligent fallback for unusual meters.',
    link: '/analyzer',
    badge: 'ML',
  },
  {
    icon: '📚',
    title: 'Meter Encyclopedia',
    desc: 'Browse 200+ Sanskrit meters with patterns, examples, descriptions, and Gaṇa sequences.',
    link: '/meters',
    badge: 'Reference',
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] },
  },
};

export default function Home() {
  return (
    <div className="home" id="home-page">
      {/* === HERO SECTION === */}
      <section className="hero" id="hero-section">
        {/* Animated background elements */}
        <div className="hero__bg">
          <div className="hero__orb hero__orb--1" />
          <div className="hero__orb hero__orb--2" />
          <div className="hero__orb hero__orb--3" />
          <div className="hero__grid-pattern" />
        </div>

        <div className="container hero__content">
          <motion.div
            className="hero__text"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] }}
          >
            <span className="badge badge--saffron hero__badge">
              Sanskrit Prosody & NLP
            </span>
            <h1 className="hero__title">
              Discover the <span className="hero__title-accent">Rhythm</span> of
              <br />
              <span className="hero__title-sanskrit devanagari">संस्कृत काव्य</span>
            </h1>
            <p className="hero__subtitle">
              Identify poetic meters, analyze sandhi patterns, translate with
              word-by-word analysis, and extract text from manuscripts — all
              powered by custom NLP and AI.
            </p>
            <div className="hero__actions">
              <Link to="/analyzer" className="btn btn--primary btn--lg" id="hero-cta-primary">
                Start Analyzing
                <span>→</span>
              </Link>
              <Link to="/about" className="btn btn--outline btn--lg" id="hero-cta-secondary">
                Learn More
              </Link>
            </div>
          </motion.div>

          {/* Demo Preview */}
          <motion.div
            className="hero__demo"
            initial={{ opacity: 0, x: 60 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3, ease: [0.25, 0.46, 0.45, 0.94] }}
          >
            <div className="hero__demo-card">
              <div className="hero__demo-header">
                <span className="hero__demo-dot" />
                <span className="hero__demo-dot" />
                <span className="hero__demo-dot" />
                <span className="hero__demo-title">Chandas Analysis</span>
              </div>
              <div className="hero__demo-body">
                <p className="hero__demo-verse devanagari">
                  वागर्थाविव सम्पृक्तौ वागर्थप्रतिपत्तये ।
                  <br />
                  जगतः पितरौ वन्दे पार्वतीपरमेश्वरौ ॥
                </p>
                <div className="hero__demo-result">
                  <span className="badge badge--success">✓ Identified</span>
                  <span className="hero__demo-meter">अनुष्टुभ् (Anuṣṭubh)</span>
                </div>
                <div className="hero__demo-pattern">
                  <span className="lg-symbol lg-symbol--guru" title="Guru">—</span>
                  <span className="lg-symbol lg-symbol--laghu" title="Laghu">◡</span>
                  <span className="lg-symbol lg-symbol--guru" title="Guru">—</span>
                  <span className="lg-symbol lg-symbol--guru" title="Guru">—</span>
                  <span className="lg-symbol lg-symbol--laghu" title="Laghu">◡</span>
                  <span className="lg-symbol lg-symbol--laghu" title="Laghu">◡</span>
                  <span className="lg-symbol lg-symbol--laghu" title="Laghu">◡</span>
                  <span className="lg-symbol lg-symbol--guru" title="Guru">—</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Scroll indicator */}
        <motion.div
          className="hero__scroll"
          animate={{ y: [0, 8, 0] }}
          transition={{ repeat: Infinity, duration: 2, ease: 'easeInOut' }}
        >
          <span>↓</span>
        </motion.div>
      </section>

      {/* === FEATURES SECTION === */}
      <section className="features-section section" id="features-section">
        <div className="container">
          <motion.div
            className="section__header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="badge badge--indigo">Features</span>
            <h2 className="section__title">10 Technical Areas, One Platform</h2>
            <p className="section__subtitle">
              From computational linguistics to deep learning — a comprehensive
              Sanskrit analysis toolkit.
            </p>
          </motion.div>

          <motion.div
            className="features-grid"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
          >
            {features.map((feature, index) => (
              <motion.div key={index} variants={itemVariants}>
                <Link to={feature.link} className="card card--feature" id={`feature-card-${index}`}>
                  <div className="card__icon">{feature.icon}</div>
                  <span className="badge badge--saffron feature__badge">{feature.badge}</span>
                  <h3 className="card__title">{feature.title}</h3>
                  <p className="card__desc">{feature.desc}</p>
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* === HOW IT WORKS === */}
      <section className="how-section section" id="how-it-works-section">
        <div className="container">
          <motion.div
            className="section__header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="badge badge--indigo">How It Works</span>
            <h2 className="section__title">Three-Tier Hybrid Architecture</h2>
            <p className="section__subtitle">
              A custom-built engine with exact matching, fuzzy search, and deep
              learning fallback.
            </p>
          </motion.div>

          <div className="how-steps">
            {[
              {
                step: '01',
                title: 'Input & Parse',
                desc: 'Enter Sanskrit text in Devanagari or IAST. Our custom syllable parser segments it using Unicode-aware phonological rules.',
              },
              {
                step: '02',
                title: 'Analyze Pattern',
                desc: 'Each syllable is classified as Laghu (light) or Guru (heavy). Gaṇa groups and Mātrā counts are computed.',
              },
              {
                step: '03',
                title: 'Identify Meter',
                desc: 'The L-G pattern is matched against 200+ meters via exact match → fuzzy search → LSTM classifier.',
              },
            ].map((item, i) => (
              <motion.div
                key={i}
                className="how-step"
                initial={{ opacity: 0, x: i % 2 === 0 ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.15 }}
              >
                <span className="how-step__number">{item.step}</span>
                <div className="how-step__content">
                  <h3 className="how-step__title">{item.title}</h3>
                  <p className="how-step__desc">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* === CTA === */}
      <section className="cta-section section" id="cta-section">
        <div className="container">
          <motion.div
            className="cta-card"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="cta-card__title devanagari">
              छन्दांसि विश्वस्य पदवीम्
            </h2>
            <p className="cta-card__subtitle">
              Start exploring the rich world of Sanskrit prosody today
            </p>
            <Link to="/analyzer" className="btn btn--primary btn--lg" id="cta-start-btn">
              Launch Chandas Analyzer →
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
