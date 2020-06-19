// @flow

import * as React from "react";
import axios from "axios";

const hostName = window.location.hostname;

class NFChain extends React.Component {

    constructor(props) {
        super();
        this.state = { ...props };
    }
    
    startHandler = e => {
        e.preventDefault();
        this.state = {
            request_type: "start"
        }
        axios.post('node1.mingyuma-QV74156.gwcloudlab-PG0.wisc.cloudlab.us:8000', this.state).then(response => {
            console.log(response)
        }).catch(error => {
            console.log(error)
        })
    }

    render() {
        return(
            <div>
                <form>
                    <button onClick={this.startHandler}>Start</button>
                </form>
            </div>
        );
    }
}

export default NFChain