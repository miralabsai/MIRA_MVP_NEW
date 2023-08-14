import React from 'react';
import TypingEffect from './typing_effect';

const BackgroundVideo = () => (
  <div className="absolute inset-0 z-20">
    <video src="/video(1080p).mp4" type="video/mp4" autoPlay loop muted className="w-full h-full object-cover" />
    <div className="absolute font-mono top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center z-50 text-dimWhite text-1xl md:text-2xl lg:text-3xl">
      <TypingEffect />
    </div>
  </div>
);

export default BackgroundVideo;
