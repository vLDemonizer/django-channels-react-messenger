import React, { Component } from 'react';
import $ from 'jquery';
import Message from './Message'

class Chat extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chat: {
                messages: [],
                id: window.chat
            },
            socket: new WebSocket('ws://localhost:8000/chat/stream/'),
        };
    }

    componentDidMount() {
        this.setupWebsocket();
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.chat) {
            this.setState({
                chat: nextProps.chat
            });
            // Log into current chat
            let message = {
                command: 'join',
                chat: nextProps.chat.id,
            };
            this.state.socket.send(JSON.stringify(message));
        }

    }

    setupWebsocket() {
        let websocket = this.state.socket;
        websocket.onopen = () => () => {
            console.log('open')
        };
    
        websocket.onmessage = (evt) => {
            if (evt.data.hasOwnProperty('command') && evt.data.hasOwnProperty('message')) {
                let conversation = this.state.chat.messages;
                console.log(evt.data.message)
                conversation.push(evt.data);
                this.setState({messages: conversation});
            }
        };
    
        websocket.onclose = () => {
            console.log('closed')
        }
    }

    componentWillUnmount() {
        this.state.ws.close();
      }

    render() {
        const user = window.user;
        const chat = this.props.chat;
        let messages = '';
        if (chat) {
            console.log(chat.messages)
            messages = chat.messages.map(message => <Message 
                key={message.id} 
                classType={chat.sender.id !== user ? 'receiver' : 'sender'} 
                text={message.text} 
                date_sent={message.date_sent} 
            />);
            console.log(messages)
        }

        return (
            <div className="col-sm-8 conversation">
                <div className="row heading">
                    <div className="col-sm-2 col-md-1 col-xs-3 heading-avatar">
                        <div className="heading-avatar-icon">
                            <img src="https://bootdey.com/img/Content/avatar/avatar6.png" alt="avatar" />
                        </div>
                    </div>
                    <div className="col-sm-8 col-xs-7 heading-name">
                        <a className="heading-name-meta">{chat ? chat.receiver.username : ''}</a>
                        <span className="heading-online">Online</span>
                    </div>
                    <div className="col-sm-1 col-xs-1  heading-dot pull-right">
                        <i className="fa fa-ellipsis-v fa-2x  pull-right" aria-hidden="true"></i>
                    </div>
                </div>
                <div className="row message" id="conversation">
                    <br />
                    {messages}
                </div>

                <div className="row reply">
                    <div className="col-sm-1 col-xs-1 reply-emojis">
                        <i className="fa fa-smile-o fa-2x"></i>
                    </div>
                    <div className="col-sm-9 col-xs-9 reply-main">
                        <textarea className="form-control" rows="1" id="comment" ref={text => { this.messageText = text; }}></textarea>
                    </div>
                    <div className="col-sm-1 col-xs-1 reply-recording">
                        <i className="fa fa-microphone fa-2x" aria-hidden="true"></i>
                    </div>
                    <div className="col-sm-1 col-xs-1 reply-send" onClick={() => {
                        let message = {
                            command: 'send',
                            chat: chat.id,
                            message: this.messageText.value,
                        };
                        this.state.socket.send(JSON.stringify(message));
                        $('#comment').val('');
                    }}>
                        <i className="fa fa-send fa-2x" aria-hidden="true"></i>
                    </div>
                </div>
            </div>
        );
    }
}  

export default Chat;