import React, { Component } from 'react';
import $ from 'jquery';
import forge from 'node-forge';
import Message from './Message';

class Chat extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chat: {
                messages: [],
                id: window.chat
            },
            type: 'rsa',
            socket: new WebSocket('ws://' + window.location.host +'/chat/stream/'),
            publicKey: '',
        };
    }

    componentDidMount() {
        this.setupWebsocket();
        if (typeof this.messagesDiv !== "undefined") {
            this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight;
        }
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

    componentDidUpdate() {
        if (typeof this.messagesDiv !== "undefined") {
            this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight;
        }
    }

    componentWillUnmount() {
        this.state.ws.close();
    }

    setupWebsocket() {
        let websocket = this.state.socket;
        websocket.onopen = () => {
            console.log('open')
        };
    
        websocket.onmessage = (evt) => {
            let data = JSON.parse(evt.data)
            if ('key' in data) {
                console.log(data)
                this.setState({
                    publicKey: forge.pki.publicKeyFromPem(data.key)
                });
            }
            else if ('message' in data) {
                let conversation = this.state.chat.messages;
                console.log(data.message)
                conversation.push(data.message)
                this.setState({messages: conversation});
            }
        };
    
        websocket.onclose = () => {
            console.log('closed')
        }
    }

    rsaEncrypt(text) {
        let encryptedMessage = this.state.publicKey.encrypt(text, "RSA-OAEP", {
            md: forge.md.sha256.create(),
            mgf1: forge.mgf1.create()
        });
        console.log(encryptedMessage)
        let messageBase64 = forge.util.encode64(encryptedMessage);
        console.log(messageBase64)
        let message = {
            command: 'send',
            chat: chat.id,
            message: messageBase64,
            user: window.user,
            type: this.state.type
        };
        this.state.socket.send(JSON.stringify(message));
    }

    aesEncrypt(text) {
        var Crypto = require('cryptojs');
        Crypto = Crypto.Crypto;

        var KEY = 'This is a key123';
        var IV = 'This is an IV456';
        var MODE = new Crypto.mode.CFB(Crypto.pad.ZeroPadding);

        var plaintext = 'The answer is no';
        var input_bytes = Crypto.charenc.UTF8.stringToBytes(plaintext);
        var key = Crypto.charenc.UTF8.stringToBytes(KEY);
        var options = {iv: Crypto.charenc.UTF8.stringToBytes(IV), asBytes: true, mode: MODE};
        var encrypted = Crypto.AES.encrypt(input_bytes, key, options);
        var encrypted_hex = Crypto.util.bytesToHex(encrypted);
        console.log(encrypted_hex); // this is the value you send over the wire

        output_bytes = Crypto.util.hexToBytes(encrypted_hex);
        output_plaintext_bytes = Crypto.AES.decrypt(output_bytes, key, options);
        output_plaintext = Crypto.charenc.UTF8.bytesToString(output_plaintext_bytes);
        console.log(output_plaintext); // result: 'The answer is no'
    }

    render() {
        const user = window.user;
        const chat = this.props.chat;
        let messages = '';
        if (this.state.chat.id === 0) {
            return <div className="col-sm-8 conversation"></div>
        }
        if (chat) {
            messages = chat.messages.map(message => <Message 
                key={message.id} 
                classType={message.sender.id !== user ? 'receiver' : 'sender'} 
                text={message.text} 
                date_sent={message.date_sent} 
            />);
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
                        <a className="heading-name-meta">
                            <span className="name-meta">
                                {!chat ? '' : chat.users[0].id != window.user ? chat.users[0].username : chat.users[1].username }
                            </span>
                        </a>
                        <span className="heading-online">Online</span>
                    </div>
                    <div className="col-sm-1 col-xs-1  heading-dot pull-right">
                        <i className="fa fa-ellipsis-v fa-2x  pull-right" aria-hidden="true"></i>
                    </div>
                </div>
                <div className="row message" id="conversation" ref={messages => {this.messagesDiv = messages;}}>
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
                        let type = this.state.type;
                        let text = this.messageText.value;
                        console.log(text);
                        if (type === 'rsa') {
                            this.rsaEncrypt(text);
                        } else {
                            this.aesEncrypt(text);
                        }
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