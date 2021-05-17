import React from 'react';
import ReactDOM from 'react-dom';
import * as Parameters from './Parameters';
import './App.css';

import Experiment from './components/Experiment'

const EXPERIMENT_MAIN_ID = "Experiment-main"

function startExperiment(event) {
    event.preventDefault()
    ReactDOM.render(
        <div>
            <Experiment/>
        </div>
    , document.getElementById(EXPERIMENT_MAIN_ID))
}

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>ReactJS Progressive Web Application</h1>
            </header>
            <main>
                <p>Param amount of elements: {Parameters.PARAMETER_CONTENT_ELEMENT_AMOUNT}</p>
                <button onClick={startExperiment}>Start experiment</button>
                <div id={EXPERIMENT_MAIN_ID}></div>
            </main>
        </div>
    );
}

export default App;
