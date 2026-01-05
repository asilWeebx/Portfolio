import React from 'react';
import ReactDOM from 'react-dom/client'; // React 18 uchun
import App from './App.jsx';

import "bootstrap/dist/css/bootstrap.min.css";

import './styles/owl.carousel.min.css';
import './styles/owl.theme.default.min.css';
import './styles/animate.min.css';
import './styles/smooth-scrollbar.css';
import './styles/lightbox.min.css';

import './styles/style.css';
import './styles/responsive.css';

// React 18 createRoot usuli
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
