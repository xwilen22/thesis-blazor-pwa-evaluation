class NodeInstance {
    constructor(data, id) {
        this.data = Number(data)
        this.childNodes = Array(0)
        this.id = Number(id)
    }
    toObject() {
        return {
            data : this.data,
            childNodes : this.childNodes,
            id : this.id
        }
    }
    addChild(element) {
        this.childNodes.push(element)
    }
    addToData(addition) {
        this.data += Number(addition)
    }
}

export default NodeInstance