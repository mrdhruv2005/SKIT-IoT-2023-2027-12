import './LoadingSpinner.css';

export default function LoadingSpinner({ size = 'md', text = '' }) {
  return (
    <div className="spinner-container" id="loading-spinner">
      <div className={`spinner spinner--${size}`}>
        <div className="spinner__ring" />
        <div className="spinner__ring spinner__ring--inner" />
        <span className="spinner__char devanagari">ॐ</span>
      </div>
      {text && <p className="spinner__text">{text}</p>}
    </div>
  );
}
