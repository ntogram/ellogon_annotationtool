import React, { Component } from "react";
import requestInstance from "../requestAPI";

class Mainview extends Component {
    constructor(props) {
        super(props);
        this.state = {
            message:"",
        };

        this.getMessage = this.getMessage.bind(this)
    }

    async getMessage(){
    try {
        let response = await requestInstance.get('/main/');
        console.log(response)
        const message = response.data.hello;
        this.setState({
            message: message,
        });
        console.log(message)
        return message;
    }catch(error){
        //console.log("Error: ", JSON.stringify(error, null, 4));
        this.props.history.push({pathname:"/sign-in"});
        throw error;
    }
}





    componentDidMount(){
        // It's not the most straightforward thing to run an async method in componentDidMount
       // window.addEventListener('onbeforeunload', this.props.handleWindowClose);

        // Version 1 - no async: Console.log will output something undefined.
        const messageData1 = this.getMessage();
        console.log(messageData1)
        console.log("messageData1: ", JSON.stringify(messageData1, null, 4));
    }

    render(){
        return (
            <div>
                <p> Hello:</p>
                <p>{this.state.message}</p>

            </div>
        )
    }
}

export default Mainview;