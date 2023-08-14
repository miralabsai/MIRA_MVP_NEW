import React from 'react';

const HeaderIndex = () => (
  <header className="relative">
    <video className="w-full" loop autoPlay muted>
      <source src="/video(1080p).mp4" type="video/mp4" />
    </video>
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center z-50">
      <h1 className="text-white text-1xl md:text-2xl lg:text-4xl">
        Discover MIRA: The Future of Mortgage Lending,<br /> Powered by Excellence and Innovation
      </h1>
    </div>
  </header>
);

export default HeaderIndex;
