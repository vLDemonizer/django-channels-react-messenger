import React, { Component } from 'react';
import $ from 'jquery';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

class ContactList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            users: []
        };
    }

    componentDidMount() {
        axios.get('/users')
            .then(response => this.setState({users: response.data}))
            .catch(error => console.log(error, 1))
    }

    render() {
        return (
            <div className="side-two">
                <div className="row newMessage-heading">
                    <div className="row newMessage-main">
                        <div className="col-sm-2 col-xs-2 newMessage-back">
                            <i className="fa fa-arrow-left" aria-hidden="true" onClick={() => {
                                $(".side-two").css({
                                    "left": "-100%"
                                });
                            }}></i>
                        </div>
                        <div className="col-sm-10 col-xs-10 newMessage-title">
                            New Chat
                        </div>
                    </div>
                </div>

                <div className="row composeBox">
                    <div className="col-sm-12 composeBox-inner">
                        <div className="form-group has-feedback">
                            <input id="composeText" type="text" className="form-control" name="searchText" placeholder="Search People" />
                        </div>
                    </div>
                </div>

                <div className="row compose-sideBar">
                    {this.state.users.map(user => 
                        <div key={user.id} className="row sideBar-body" onClick={() => {
                            let data = new URLSearchParams();
                            data.append('receiver', user.id);
                            data.append('sender', window.user);
                            axios.post('/create-chat/', data)
                                .then(response => {
                                    console.log(response)
                                    this.props.updateMainChat(response.data)
                                })
                                .catch(error => console.log(error, 2));
                            
                            $(".side-two").css({
                                "left": "-100%"
                            });
                        }}>
                            <div className="col-sm-3 col-xs-3 sideBar-avatar">
                                <div className="avatar-icon">
                                    <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt='avatar' />
                                </div>
                            </div>
                            <div className="col-sm-9 col-xs-9 sideBar-main">
                                <div className="row">
                                    <div className="col-sm-8 col-xs-8 sideBar-name">
                                        <span className="name-meta">{user.username}</span>
                                    </div>
                                    <div className="col-sm-4 col-xs-4 pull-right sideBar-time">
                                        <span className="time-meta pull-right">{user.last_login}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

export default ContactList;