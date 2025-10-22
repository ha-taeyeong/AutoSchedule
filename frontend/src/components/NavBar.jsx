// src/components/NavBar.jsx
import React from "react";
import { HashLink } from "react-router-hash-link";

const NavBar = () => (
  <div className="fixed w-full h-[164px] top-0 left-0 bg-white z-50 shadow">
    <div className="inline-flex items-center justify-end gap-8 absolute top-14 left-[1300px]">
      <HashLink
        to="#about"
        scroll={el => {
          const y = el.getBoundingClientRect().top + window.pageYOffset - NAV_HEIGHT - EXTRA_GAP;
          window.scrollTo({ top: y, behavior: "smooth" });
        }}>
        About
      </HashLink>

      <HashLink
        to="/#skills-section"
        smooth
        className="relative w-fit font-body-text font-[number:var(--body-text-font-weight)] 
          text-black text-[length:var(--body-text-font-size)] tracking-[var(--body-text-letter-spacing)] 
          leading-[var(--body-text-line-height)] whitespace-nowrap [font-style:var(--body-text-font-style)] cursor-pointer"
      >
        Skills
      </HashLink>
      <a
        href="http://13.210.90.100.nip.io/"
        target="_blank"
        rel="noopener noreferrer"
        className="relative w-fit font-body-text font-[number:var(--body-text-font-weight)]  
          text-black text-[length:var(--body-text-font-size)] tracking-[var(--body-text-letter-spacing)] 
          leading-[var(--body-text-line-height)] whitespace-nowrap [font-style:var(--body-text-font-style)] cursor-pointer"
      >
        Memo
      </a>
      <HashLink
        to="/#contact-section"
        smooth
        className="relative w-fit font-body-text font-[number:var(--body-text-font-weight)] 
          text-black text-[length:var(--body-text-font-size)] tracking-[var(--body-text-letter-spacing)] 
          leading-[var(--body-text-line-height)] whitespace-nowrap [font-style:var(--body-text-font-style)] cursor-pointer"
      >
        Contact
      </HashLink>
    </div>
    <img
        className="absolute w-[184px] h-[88px] top-[38px] left-[86px] object-cover cursor-pointer"
        alt="Image"
        src="https://c.animaapp.com/kPFgkC5m/img/image-21@2x.png"
        onClick={() => window.location.href = "/"}
        />
     </div>
);

export default NavBar;
