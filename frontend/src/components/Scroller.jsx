import React, { useState } from 'react';
import './Scroller.css';

const topics = [
    {
      title: 'Meet MIRA',
      description:
        'Discover the innovation behind MIRA, your Mortgage Intelligent Processing Assistant. Designed with expertise and tailored to your needs, MIRA transforms mortgage lending into a seamless and personalized experience. Step into the future of lending with MIRA by your side.',
    },
    {
      title: "MIRA's Magic",
      description: 'Embark on a journey where technology meets intuition. MIRA\`s Magic is the ability to simplify complex processes, guiding you effortlessly from eligibility to application. With a touch of magic, MIRA ensures a smooth and efficient mortgage journey, making dreams come true.',
    },
    {
      title: "MIRA's Mastery",
      description: 'Unleash the full potential of mortgage lending with MIRA\'s Mastery. Our comprehensive toolset empowers both lenders and applicants, ensuring clarity, efficiency, and accuracy at every step. Harness the mastery of MIRA and redefine what\'s possible in the mortgage landscape.',
    },
    {
        title: "MIRA's Care",
        description: 'Your questions, our priority. MIRA\'s Care is about being there when you need us. Whether you need a detailed explanation of mortgage options or assistance with document submission, our support team, powered by AI, ensures you\'re never left in the dark. We\'re here to guide, assist, and care.',
    },
    {
        title: "Unlock MIRA",
        description: 'Signup/Login to unlock MIRA\'s Magic, Mastery, and Care.'
    }
  ];
  

  const Scroller = () => {
    const [selected, setSelected] = useState(null);
  
    return (
      <div className="flex-container">
        <div className="spinner">
          <p>
            <div className="cube1"></div>
            <div className="cube2"></div>
            Loading...
          </p>
        </div>
        {topics.map((topic, index) => (
          <div
            key={index}
            className={`flex-slide z-20 ${selected === topic.title ? 'selected' : ''}`}
            onClick={() => setSelected(selected === topic.title ? null : topic.title)}
          >
            <div className="flex-title z-20">{topic.title}</div>
            <div className="flex-about z-20">
              <p>{topic.description}</p>
            </div>
          </div>
        ))}
      </div>
    );
  };
  

export default Scroller;
