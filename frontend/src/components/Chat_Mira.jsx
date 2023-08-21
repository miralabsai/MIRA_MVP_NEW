import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { DotWave } from '@uiball/loaders';
import './Dashboard.css';

function Chat_Mira() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef(null);
  const chatHistoryRef = useRef(null);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);

  const formatText = (text) => {
    return text.split('\n').map((line, index, array) => (
      <React.Fragment key={index}>
        {line}
        {index < array.length - 1 && <br />}
      </React.Fragment>
    ));
  };

  const scrollToBottom = () => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom(); // Scroll to the bottom whenever the chat history changes
  }, [chatHistory]);

  const sendMessage = async () => {
    if (isWaitingForResponse) return; // Prevent sending if waiting for response
    // Add the user message to the chat history
    setChatHistory((prevChatHistory) => [...prevChatHistory, { text: message, user: 'user' }]);
    setIsLoading(true); // Start loading animation
    const userMessage = message; // Store the user's message
    setMessage(''); // Clear the message input
    setIsWaitingForResponse(true); // Set the waiting flag to true
    try {
      // Make a POST request to the backend to get the response
      const response = await axios.post(
        'http://localhost:8001/converse', // Update this URL to your backend endpoint
        { query: userMessage }
      );
      // Add the AI response to the chat history
      setChatHistory((prevChatHistory) => [...prevChatHistory, { text: response.data.response, user: 'mira' }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
    setIsLoading(false); // Stop loading
    setIsWaitingForResponse(false); // Set waiting for response to false
  };

  const handleSendMessage = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(); // Call the sendMessage function when Enter is pressed
    }
  };

  const handleTextareaChange = (e) => {
    setMessage(e.target.value);
    const textarea = textareaRef.current;
    textarea.style.height = 'auto'; // Reset height to auto to recalculate
    textarea.style.height = `${textarea.scrollHeight}px`; // Set height to scrollHeight
  };

  useEffect(() => {
    const textarea = textareaRef.current;
    textarea.style.height = 'auto'; // Reset height to auto to recalculate
    textarea.style.height = `${textarea.scrollHeight}px`; // Set height to scrollHeight
  }, []);


  return (
    <div className="chat-container">
      <div className="chat-input-container">
        <div className="chat-history" ref={chatHistoryRef}> {/* Add the reference here */}
          {chatHistory.map((msg, index) => (
            <div key={index} className={`chat-bubble ${msg.user}`}>
              {formatText(msg.text)} {/* Call the formatText function here */}
            </div>
          ))}
          {isLoading && <DotWave size={24} speed={1} color="black" />}
        </div>
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={handleTextareaChange}
            onKeyPress={handleSendMessage}
            className="chat-input"
            rows={1}
            style={{ overflowY: 'auto', maxHeight: '200px' }} // Scroll after reaching maxHeight
            disabled={isWaitingForResponse} // Disable the input if waiting for response
          />
          <button onClick={sendMessage} className="send-button" disabled={isWaitingForResponse}> {/* Call the sendMessage function when the button is clicked */}
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat_Mira;
