import React, { Component } from 'react';
import './App.css';
import Chat from './components/Chat';
import ChatList from './components/ChatList';
import ContactList from './components/ContactList';
import axios from 'axios';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      mainChat: null,
      chats: [],
    }
  }

  componentDidMount() {
    axios.get('/chats')
      .then(response => this.setState({
        chats: response.data,
        mainChat: response.data[0]
      }))
      .catch(error => console.log(error))
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
                .catch(error => console.log(error))
            }
          } 
        />
      </div>,
      <Chat key={2} chat={this.state.mainChat} />,
    ];
  }
}

export default App;
