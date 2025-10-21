// src/components/FixedNavBar.jsx

import React from "react";

// ⚠️ MainPage.jsx에서 FixedNavBar를 사용할 때 projectName="AutoSchedule"와 같이 prop을 전달한다고 가정합니다.

const navItems = [
  // 1. 문제 해결 및 가치 증명 섹션으로 연결
  { name: "Why AutoSchedule", href: "#problem-solution" }, 
  // 2. 작동 방식 (AI 로직) 섹션으로 연결
  { name: "How It Works", href: "#how-it-works" },
  // 3. (제거됨) Pricing 섹션
  // { name: "Pricing", href: "#pricing" }, 
  // 4. 개발자 연락처/포트폴리오 섹션으로 연결
  { name: "Contact Developer", href: "#contact" }, 
];

const FixedNavBar = ({ projectName = "AutoSchedule" }) => { // 기본값으로 AutoSchedule 설정
  return (
    <nav 
      className="fixed top-0 left-0 w-full bg-white shadow-md z-40"
      style={{ height: '100px' }} // MainPage.jsx의 NAV_HEIGHT와 일치
    >
      <div className="max-w-7xl mx-auto px-6 h-full flex justify-between items-center">
        
        {/* 1. 로고/프로젝트명: 'Plan Up' 텍스트/이미지를 'AutoSchedule'로 변경 */}
        <a href="/" className="flex items-center space-x-2">
          {/* 로고 이미지를 AutoSchedule 컨셉에 맞게 변경해야 합니다. */}
          {/* 현재 이미지를 대체하여 임시로 텍스트와 아이콘을 사용합니다. */}
          <span className="font-pretendard text-3xl font-black text-blue-600">
            {projectName}
          </span>
          <span className="text-sm font-semibold text-gray-500 hidden sm:inline">
            | 하태영 포트폴리오
          </span>
        </a>

        {/* 2. 네비게이션 링크 그룹 */}
        <div className="flex space-x-8">
          {navItems.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className="font-pretendard text-lg font-medium text-gray-700 hover:text-blue-600 transition duration-150"
            >
              {item.name}
            </a>
          ))}
          
          {/* ⚠️ 기존의 'Memo' 메뉴는 비즈니스 UI에 맞지 않아 제거되었습니다. */}
          
        </div>
      </div>
    </nav>
  );
};

export default FixedNavBar;