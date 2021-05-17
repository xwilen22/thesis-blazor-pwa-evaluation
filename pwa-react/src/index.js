import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as minimalServiceWorkerRegistration from './minServiceWorkerRegistration'

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

minimalServiceWorkerRegistration.registerMinServiceWorker();