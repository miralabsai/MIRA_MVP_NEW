import React, { useState, useEffect } from 'react';

const TypingEffect = () => {
  const texts = [
    '"UNVEILING MIRA"',
    'Mortgage Lending Reimagined',
    'Powered by Excellence and AI Innovation',
  ];
  const [lines, setLines] = useState(Array(texts.length).fill(''));
  const [lineIndex, setLineIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);

  useEffect(() => {
    if (charIndex < texts[lineIndex].length) {
      const timeout = setTimeout(() => {
        setLines((prevLines) => {
          const newLines = [...prevLines];
          newLines[lineIndex] += texts[lineIndex][charIndex];
          return newLines;
        });
        setCharIndex((prevCharIndex) => prevCharIndex + 1);
      }, 100); // Typing speed

      return () => clearTimeout(timeout);
    } else {
      setTimeout(() => {
        setCharIndex(0);
        if (lineIndex < texts.length - 1) {
          setLineIndex((prevLineIndex) => prevLineIndex + 1);
        } else {
          setLineIndex(0);
          setLines(Array(texts.length).fill('')); // Reset all lines to start over
        }
      }, 2000); // Delay before starting the next line
    }
  }, [lines, lineIndex, charIndex, texts]);

  return (
    <div>
      {lines.map((line, index) => (
        <div key={index}>
          <span>{line}</span>
          <br />
        </div>
      ))}
    </div>
  );
};

export default TypingEffect;
