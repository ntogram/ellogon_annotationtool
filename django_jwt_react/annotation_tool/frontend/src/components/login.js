import React, { Component } from "react";
import requestInstance from "../requestAPI";
import { useHistory } from "react-router-dom";
class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {email: "", password: "",remember:false};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCheckboxChange= this.handleCheckboxChange.bind(this)


         //console.log(this.props.location)
    }

    handleCheckboxChange(event){

       this.setState({

      remember:!this.state.remember
    })

      // console.log(event.target.checked)
       //console.log(this.state.remember)

       // console.log(target.checked==false)
    }


    handleChange(event) {



        this.setState({[event.target.name]: event.target.value});
        console.log(event.target.value)

    }
async handleSubmit(event) {
    event.preventDefault();
   console.log(this.state.remember)
    try {
        const response = await requestInstance.post('/token/obtain/', {
            email: this.state.email,
            password: this.state.password
        });

        const data=response.data
        requestInstance.defaults.headers['Authorization'] = "JWT " + data.access;
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('email',this.state.email);
        localStorage.setItem('remember',this.state.remember);
        console.log("data_access: "+data.access)
        console.log("data_refresh: "+data.refresh)
        this.props.history.push("/main")

        return data;
    } catch (error) {
         this.props.history.push({
                pathname: '/sign-in',
                search: '',
                state: 0
            })
    }

}






  /*  handleSubmit(event) {
        event.preventDefault();

       requestInstance.post('/token/obtain/', {
            email: this.state.email,
            password: this.state.password
        }).then(
            result => {
                requestInstance.defaults.headers['Authorization'] = "JWT " + result.data.access;
                localStorage.setItem('access_token', result.data.access);
                localStorage.setItem('refresh_token', result.data.refresh);
            }
    ).catch (error => {
        throw error;
    })
    }
*/
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <h3>Sign In</h3>
     <div style={{display:(this.props.location.state==0) ? "block":"none"}}  className="alert alert-danger" role="alert">Wrong Credentials </div>
                <div className="form-group">
                    <label>Email address</label>
                    <input name="email" type="email" value={this.state.email} onChange={this.handleChange} className="form-control" placeholder="Enter email" required />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input name="password" type="password" value={this.state.password} onChange={this.handleChange} className="form-control" placeholder="Enter password" required/>
                </div>

                <div className="form-group">
                    <div className="custom-control custom-checkbox">
                        <input  name="remember" type="checkbox" className="custom-control-input" id="customCheck1"  checked={this.state.remember} onChange={this.handleCheckboxChange}/>
                        <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>

                    </div>
                </div>

                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                <p className="forgot-password text-right">
                    Forgot <a href="/forget_password">password?</a>
                </p>
            </form>
        )
    }
}
export default Login;