import React, { useState } from 'react'; // Import useState
import './Dashboard.css';

function Chat_Mira() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]); // Initialize chatHistory

  const handleSendMessage = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent default Enter behavior
      // Logic to send the message to the backend
      // Add the message to the chat history
      setChatHistory([...chatHistory, { text: message, user: 'user' }]);
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
        </div>
        <div className="input-wrapper"> {/* Added input-wrapper */}
          <textarea
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleSendMessage} // Added onKeyPress
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
