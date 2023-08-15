import React, { useState } from 'react';
import axios from 'axios'; // Import axios
import { DotWave } from '@uiball/loaders'; // Import DotWave loader
import './Dashboard.css';

function Chat_Mira() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      // Add the user message to the chat history
      setChatHistory((prevChatHistory) => [...prevChatHistory, { text: message, user: 'user' }]);
      setIsLoading(true); // Start loading animation
      try {
        // Make a POST request to the backend to get the response
        const response = await axios.post(
          'http://localhost:8001/converse', // Update this URL to your backend endpoint
          { query: message }
        );
        // Add the AI response to the chat history
        setChatHistory((prevChatHistory) => [...prevChatHistory, { text: response.data.response, user: 'mira' }]);
      } catch (error) {
        console.error('Error sending message:', error);
      }
      setIsLoading(false); // Stop loading
      setMessage('');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-input-container">
        <div className="chat-history">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`chat-bubble ${msg.user}`}>
              {msg.text}
            </div>
          ))}
          {isLoading && <DotWave size={24} speed={1} color="black" />} {/* Render loader if isLoading is true */}
        </div>
        <div className="input-wrapper">
          <textarea
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleSendMessage}
            className="chat-input"
            rows={1}
          />
          <button onClick={handleSendMessage} className="send-button">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat_Mira;
