import React, {Component} from 'react'

class TreeElement extends Component {
    state = {
        data: this.props.data
    }
    constructor(props) {
        super(props)
        this.child = [this.props.childNodes.length]
    }
    render() {
        if(this.state.data != null) {
            return (            
                <React.Fragment>
                    <div>
                        <p>Data {this.state.data}</p>
                        {this.formatChildNodes(this.props.childNodes)}
                    </div>
                </React.Fragment>
            )
        }
        else {
            return null
        }
    }
    updateData(rootInstance) {
        if(rootInstance != null && rootInstance.data !== undefined) {
            this.setState({data: rootInstance.data})
            for(let index = 0; index < rootInstance.childNodes.length; index++) {
                this.child[index].updateData(rootInstance.childNodes[index])
            }
        }
    }
    // Formats an array of childNode states
    formatChildNodes(childNodes) {
        if (!Array.isArray(childNodes)) {
            return null
        }
        else {
            if(childNodes.length <= 0) {
                return null
            }
        }
        return (
            <React.Fragment>
                {childNodes.map((childNode, index) =>
                    <TreeElement key={childNode.id} childNodes = {childNode.childNodes} data = {childNode.data} ref={Ref => this.child[index]=Ref}/>
                )}
            </React.Fragment>
        )
    }
}

export default TreeElement