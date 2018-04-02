import React, { Component } from 'react';

class ChatList extends Component {
    render() {
        return (
            <div className="side-one">
                <div className="row heading">
                    <div className="col-sm-3 col-xs-3 heading-avatar">
                        <div className="heading-avatar-icon">
                            <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar" />
                        </div>
                    </div>
                    <div className="col-sm-4 col-xs-1 heading-name ">
                        <a className="heading-name-meta">{window.username}</a>
                    </div>
                    <div className="col-sm-1 col-xs-1  heading-dot  pull-right">
                        <a href="/logout"><i className="fa fa-ellipsis-v fa-2x  pull-right" aria-hidden="true"></i></a>
                    </div>
                    <div className="col-sm-2 col-xs-2 heading-compose  pull-right">
                        <i className="fa fa-comments fa-2x  pull-right" aria-hidden="true"></i>
                    </div>
                </div>

                <div className="row searchBox">
                    <div className="col-sm-12 searchBox-inner">
                        <div className="form-group has-feedback">
                            <input id="searchText" type="text" className="form-control" name="searchText" placeholder="Search" />
                        </div>
                    </div>
                </div>

                <div className="row sideBar">
                    {this.props.chats.map(chat =>
                        <div key={chat.id} className="row sideBar-body" onClick={() => this.props.updateMainChat(chat)}>
                            <div className="col-sm-3 col-xs-3 sideBar-avatar">
                                <div className="avatar-icon">
                                    <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt='receiver user img'/>
                                </div>
                            </div>
                            <div className="col-sm-9 col-xs-9 sideBar-main">
                                <div className="row">
                                    <div className="col-sm-8 col-xs-8 sideBar-name">
                                        <span className="name-meta">{chat.users[0].id != window.user ? chat.users[0].username : chat.users[1].username }
                                        </span>
                                    </div>
                                    <div className="col-sm-4 col-xs-4 pull-right sideBar-time">
                                        <span className="time-meta pull-right">{
                                            chat.messages[0] ? chat.messages[0].date_sent : ''
                                            }
                                        </span>
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

export default ChatList;