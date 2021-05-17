import React, {Component} from 'react'
import ReactDOM from 'react-dom';

import * as Parameters from '../Parameters'
import TreeElement from './TreeElement'
import NodeInstance from '../models/NodeInstance'

let DistributableElementsAmount = Parameters.PARAMETER_CONTENT_ELEMENT_AMOUNT

const EXPERIMENT_MAIN_ID = "EXPERIMENT_MAIN_ID"


const INTERVAL_TIME_MILLISECONDS = 1000

/// <summary>
/// Modifies tree data
/// </summary>
/// <param name="rootNode">Root of tree</param>

function scrambleTree(rootNode) {
    rootNode.data += 1
    if(rootNode.childNodes.length <= 0)
    {
        return rootNode;
    }

    for(let childElement of rootNode.childNodes)
    {
        childElement = scrambleTree(childElement);
    }

    return rootNode
}

function addElement(data, treeDepth) {
    let elementToBeAdded = new NodeInstance(data, DistributableElementsAmount)

    DistributableElementsAmount--
    if(treeDepth > 0) {
        for(let i = 0; i < Parameters.PARAMETER_MAXIMUM_CHILD_NODE_AMOUNT; i++) {
            if(DistributableElementsAmount > 0) {
                elementToBeAdded.addChild(addElement(data + 1, treeDepth - 1))
            }
            else {
                break
            }
        }
    }
    return elementToBeAdded.toObject();
}

class Experiment extends Component {
    constructor(props) {
        super(props)
        this.updateDataRef = React.createRef()
    }
    state = {
        passedSeconds: 0,
        rootElement: addElement(1, Parameters.PARAMETER_MAXIMUM_TREE_DEPTH_AMOUNT)
    }
    componentDidMount() {
        //Initialises tree
        ReactDOM.render(
            <div>
                <TreeElement childNodes = {this.state.rootElement.childNodes} data = {this.state.rootElement.data} ref={Ref => this.child=Ref}/>
            </div>
        , document.getElementById(EXPERIMENT_MAIN_ID))
        //Starts timer

        let experimentIntervalId = window.setInterval(() => {this.onTick(this, experimentIntervalId)}, INTERVAL_TIME_MILLISECONDS)
    }
    onTick(instance, intervalId) {        
        instance.setState({rootElement: scrambleTree(instance.state.rootElement)}) 

        this.child.updateData(this.state.rootElement)

        //One second passes
        instance.setState({passedSeconds: this.state.passedSeconds + 1})

        //When the time is over
        if(instance.state.passedSeconds >= Parameters.PARAMETER_EXPERIMENT_TIME_SECONDS) {
            clearInterval(intervalId)
            instance.onRemoveTree()
        }
    }
    onRemoveTree() {
        let currentRootElement = this.state.rootElement
        //Remove tree here

        for(let index = 0; index < this.state.rootElement.childNodes.length; index++) {
            currentRootElement.childNodes.pop()
        }
        currentRootElement.data = null
        this.setState({rootElement: currentRootElement})
        this.child.updateData(this.state.rootElement)
    }
    render() {
        return (
            <React.Fragment>
                <div id={EXPERIMENT_MAIN_ID}></div>
            </React.Fragment>
        )
    }
}

export default Experiment