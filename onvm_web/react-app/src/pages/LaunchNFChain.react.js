// @flow
import axios from "axios";

import React, { Component } from "react";

const hostName = window.location.hostname;

class LaunchNFChainPage extends Component {
  state = {
    selectedFile: null
  };

  // handle file change
  onFileChange = event => {
    this.setState({
      selectedFile: event.target.files[0],
      launch: 0
    });
  };

  // handle submit event
  submitHandler = event => {
    this.state = {
      request_type: "stop"
    };

    axios
      .post(`http://${hostName}:8000`, this.state)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
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

    console.log(this.state.selectedFile);

    this.state = {
      request_type: "start",
      data: formData
    };

    axios
      .post(`http://${hostName}:8000`, this.state)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });

    this.setState({
      launch: 1
    });
  };

  // read file data
  fileData = () => {
    if (this.state.selectedFile) {
      return (
        <div>
          <h2>Selected Config File:</h2>
          <p>File Name: {this.state.selectedFile.name}</p>
          <p>File Type: {this.state.selectedFile.type}</p>
        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h3>Select JSON Config File</h3>
        </div>
      );
    }
  };

  // handle terminate
  terminateButotn = () => {
    if (this.state.launch) {
      return (
        <div>
          <form ref="form" onSubmit={this.submitHandler}>
            <button type="submit">Terminate</button>
          </form>
        </div>
      );
    }
  };

  render() {
    return (
      <div>
        <h1>NF Chain Deployment</h1>
        <h3>Upload a JSON Configuration File to Launch a Chain of NFs</h3>
        <div>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>Launch</button>
          {this.terminateButton()}
        </div>
        {this.fileData()}
      </div>
    );
  }
}

export default LaunchNFChainPage;