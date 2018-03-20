import React, { Component } from 'react';

class Message extends Component {
    render () {
        return (
            <div className="row message-body">
                <div className={"col-sm-12 message-main-" + this.props.classType}>
                    <div className={this.props.classType}>
                        <div className="message-text">{this.props.text}</div>
                        <span className="message-time pull-right">{this.props.date_sent}</span>
                    </div>
                </div>
            </div>
        )
    }
}

export default Message;