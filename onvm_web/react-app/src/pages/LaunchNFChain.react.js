// @flow
import axios from "axios";

import React, { Component } from "react";

const hostName = window.location.hostname;

class LaunchNFChainPage extends Component {
  state = {
    selectedFile: null
  };

  componentDidMount() {
    window.addEventListener('beforeunload', (event) => {
        event.preventDefault();
        event.returnValue = "Closing this tab will also close the nf chain, are you sure you want to leave?"
        return this.OnStopHandler()
    });
  }

  componentWillUnmount() {
    window.removeEventListener('beforeunload', (event) => {
        return NaN
    });
  }

  // handle file change
  onFileChange = event => {
    this.setState({
      selectedFile: event.target.files[0],
      launch: 0
    });
  };

  // handle submit event
  OnStopHandler = event => {
    this.state = {
      request_type: "stop"
    };

    axios
      .post(`http://${hostName}:8000`, this.state)
      .then(response => {
        console.log(response);
        alert("Post request succeeded. Status: " + response.statusText);
      })
      .catch(error => {
        console.log(error);
        alert(error);
      });

    this.setState({
      launch: 0
    });
  };

  // handle upload file
  onFileUpload = () => {
    const formData = new FormData();

    formData.append(
      "configFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );

    var config = {
      headers: { "Content-Type": "multipart/form-data" }
    };

    console.log(this.state.selectedFile);

    axios
      .post(`http://${hostName}:8000`, formData, config)
      .then(response => {
        console.log(response);
        alert("Post request succeeded. Status: " + response.statusText);
      })
      .catch(error => {
        console.log(error);
        alert(error);
      });
  };

  // handle launch nf chain
  onLaunchChain = () => {
    this.state = {
      request_type: "start"
    };
    axios
      .post(`http://${hostName}:8000`, this.state)
      .then(response => {
        console.log(response);
        alert("Post request succeeded. Status: " + response.statusText);
      })
      .catch(error => {
        console.log(error);
        alert(error);
      });
    this.setState({
      launch: 1
    });
  };

  render() {
    return (
      <div
        style={{
          marginLeft: "50px"
        }}
      >
        <br />
        <h1>Network Function Chain Deployment</h1>
        <h4>Upload a JSON Configuration File to Launch a Chain of NFs</h4>
        <p>
          Ensure your ONVM manager is running before uploading and launching
          your chain of NFs. Navigate to the various dashboards on ONVM web to
          observe NF behavior.
          <br />
          Output from each NF will be written to the directory specified in your
          file or to a default timestamped directory.
        </p>
        <p>
          Follow the{" "}
          <a href="https://github.com/catherinemeadows/openNetVM/blob/configScript/docs/NF_Dev.md">
            documentation
          </a>{" "}
          in the ONVM repository to learn more about proper formatting for your
          config file. See an{" "}
          <a href="https://github.com/catherinemeadows/openNetVM/blob/configScript/examples/example_chain.json">
            example
          </a>{" "}
          config file.
        </p>
        <div>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>Upload</button>
          <br />
          <br />
          <button
            onClick={this.onLaunchChain}
            style={{
              backgroundColor: "#48cf7c",
              borderRadius: "4px",
              border: "none",
              padding: "14px 28px"
            }}
          >
            Launch NF Chain
          </button>
          <button
            onClick={this.OnStopHandler}
            style={{
              margin: "5px",
              backgroundColor: "#db4d5b",
              borderRadius: "4px",
              border: "none",
              padding: "14px 28px"
            }}
          >
            Terminate
          </button>
        </div>
      </div>
    );
  }
}

export default LaunchNFChainPage;