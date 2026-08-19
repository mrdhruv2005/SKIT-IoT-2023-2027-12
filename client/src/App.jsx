import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import Home from './pages/Home';
import ChandasAnalyzer from './pages/ChandasAnalyzer';
import Translator from './pages/Translator';
import OcrPage from './pages/OcrPage';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import MeterReference from './pages/MeterReference';

function AppContent() {
  return (
    <div className="app" id="chandas-app">
      <Navbar />
      <main style={{ paddingTop: 'var(--navbar-height)' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyzer" element={<ChandasAnalyzer />} />
          <Route path="/translator" element={<Translator />} />
          <Route path="/ocr" element={<OcrPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About />} />
          <Route path="/meters" element={<MeterReference />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}
