import React, { Component } from 'react';
import './App.css';
import Chat from './components/Chat';
import ChatList from './components/ChatList';
import ContactList from './components/ContactList';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      mainChat: null,
      chats: [],
      user: ''
    };
  }

  componentDidMount() {
    axios.get('/chats')
      .then(response => this.setState({
        chats: response.data,
        mainChat: response.data[0]
      }))
      .catch(error => console.log(error,4));
    axios.get('/users/' + window.user + '/')
      .then(response => this.setState({
        user: response.data
      }))
      .catch(error => console.log(error,3));
  }
  
  render() {
    return [
      <div key={1} className="col-sm-4 side">
        <ChatList chats={this.state.chats} updateMainChat={chat => this.setState({mainChat: chat})}/>
        <ContactList updateMainChat={chat => {
              this.setState({mainChat: chat})
              axios.get('/chats')
                .then(response => this.setState({
                  chats: response.data
                }))
                .catch(error => console.log(error,5))
            }
          } 
        />
      </div>,
      <Chat key={2} chat={this.state.mainChat} />,
    ];
  }
}

export default App;
