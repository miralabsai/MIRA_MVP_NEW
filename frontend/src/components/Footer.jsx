import React from 'react';

const FooterNav = () => (
  <footer className="absolute text-dimWhite bottom-0 font-semibold left-0 w-full p-4 flex justify-between bg-transparent z-20">
    <div>
      {/* Contact Us */}
      <a href="mailto:contact@example.com">Created/Developed By: Suketu Gaglani</a>
    </div>
    <div>
      {/* Copyright Comment */}
      &copy; 2023 MIRA
    </div>
  </footer>
);

export default FooterNav;
