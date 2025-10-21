// src/pages/MainPage.jsx
import React, { useEffect } from "react";
import FixedNavBar from "../../components/FixedNavBar";

// 상수 정의
const NAV_HEIGHT = 100; // FixedNavBar 높이(px)
const EXTRA_GAP = 24;   // 추가 여백(px)

// ===== 유틸리티 함수 =====
/**
 * URL 해시를 기반으로 FixedNavBar 높이를 고려하여 스크롤 위치를 조정합니다.
 */
const scrollHashWithOffset = () => {
  if (window.location.hash) {
    const id = window.location.hash.replace("#", "");
    const element = document.getElementById(id);
    if (element) {
      const yOffset = element.getBoundingClientRect().top + window.pageYOffset - NAV_HEIGHT - EXTRA_GAP;
      window.scrollTo({ top: yOffset, behavior: "smooth" });
    }
  }
};

// ===== 데이터 정의 =====

// 1. How It Works 섹션 데이터
const howItWorksSteps = [
  {
    step: 1,
    title: "Step 1 <br /> 메모만 하세요",
    description: "로그인 후, 평소처럼 일정을 텍스트로 입력하세요. 이 화면이 'AI 분석의 시작점'입니다.",
    icon: "/images/icon-input.png", 
  },
  {
    step: 2,
    title: "Step 2 <br /> AI가 자동으로 분석합니다",
    description: "지능형 시스템이 입력된 문장에서 날짜, 시간, 장소, 참석자 등 핵심 요소를 신속하게 추출합니다.",
    icon: "/images/icon-analyze.png", 
  },
  {
    step: 3,
    title: "Step 3 <br /> 캘린더에 완벽 동기화",
    description: "추출된 정보는 '테이블 형태의 일정 등록 화면'에 표시됩니다. 단 한 번의 확인/수정 후 등록이 완료됩니다.",
    icon: "/images/icon-sync.png", 
  },
];

// 2. 핵심 기능 시각화 데이터 (Demo & Key Features 섹션용)
const keyFeatures = [
    {
        title: "자연어 처리 (NLP)",
        description: "사용자가 입력한 복잡한 문맥을 정확하게 파싱하여 핵심 일정 요소(날짜, 시간, 장소)를 추출합니다.",
        iconSvgPath: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
        color: "bg-purple-100 text-purple-700",
    },
    {
        title: "중복/충돌 자동 검사",
        description: "새 일정을 등록하기 전, 모든 캘린더를 실시간으로 스캔하여 시간 충돌 가능성을 즉시 경고합니다.",
        iconSvgPath: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
        color: "bg-red-100 text-red-700",
    },
    {
        title: "통합 캘린더 싱크",
        description: "Google Calendar, Outlook 등 사용자가 사용하는 모든 플랫폼에 One-Click 연동을 제공하여 즉시 동기화를 완료합니다.",
        iconSvgPath: "M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14",
        color: "bg-green-100 text-green-700",
    },
];

// 3. Pricing 섹션 데이터는 기술 미구현으로 인해 제거됨.
// const pricingTiers = [...] // (데이터 정의 제거)


// ===== MainPage 컴포넌트 =====
const MainPage = () => {
  
  // 컴포넌트 마운트 및 해시 변경 시 스크롤 조정
  useEffect(() => {
    setTimeout(scrollHashWithOffset, 300);
    window.addEventListener('hashchange', scrollHashWithOffset);
    return () => window.removeEventListener('hashchange', scrollHashWithOffset);
  }, []);

  // 문서 제목 설정
  useEffect(() => {
    document.title = "AutoSchedule | 하태영 포트폴리오";
  }, []);

  return (
    <div className="bg-white min-h-screen w-full">
      {/* 🚩 FixedNavBar 수정 필요: 가격 링크 제거 */}
      <FixedNavBar projectName="AutoSchedule" /> 
      <main className="pt-[calc(100px+1rem)] max-w-7xl mx-auto px-6">

        {/* 1. Hero Section: 핵심 가치 제안 */}
        <section className="mb-40 pt-16 bg-gray-900 text-white rounded-3xl shadow-2xl relative overflow-hidden p-12 md:p-20"
                 style={{ backgroundImage: "url(/images/bg-abstract-dots.png)", backgroundSize: 'cover' }}>
            <div className="max-w-4xl mx-auto text-center">
                <p className="font-pretendard text-lg font-medium text-blue-400 mb-4 uppercase tracking-widest">
                    AutoSchedule: Smart Schedule Automation
                </p>
                <h1 className="font-pretendard text-5xl md:text-7xl font-black mb-8 leading-snug">
                    수고로움 <span className="text-green-400">90% 절감.</span> <br className="hidden sm:inline"/> AI가 일정 등록의 비효율을 끝냅니다.
                </h1>
                <p className="font-pretendard text-xl text-gray-300 mb-12 max-w-3xl mx-auto">
                    바쁜 전문가와 팀의 비효율을 해결하기 위해, 본 개발자가 직접 자연어 메모를 <br />
                    캘린더로 자동 동기화하는 AI 솔루션을 구현하여 수작업 비용을 획기적으로 절감합니다.
                </p>
                
                {/* CTA 버튼 그룹 */}
                <div className="flex justify-center gap-4">
                    <a 
                        href="/login" // 실제 로그인 화면으로 연결
                        className="px-8 py-4 bg-blue-500 text-white text-xl font-bold rounded-xl hover:bg-blue-600 transition duration-300 shadow-lg"
                    >
                        구글 로그인으로 시작하기
                    </a>
                    <a 
                        href="#contact"
                        className="px-8 py-4 border-2 border-gray-500 text-gray-200 text-xl font-bold rounded-xl hover:bg-gray-700 transition duration-300"
                    >
                        기술 문의 및 포트폴리오 확인 →
                    </a>
                </div>

                {/* 정량적 지표 컴포넌트 */}
                <div className="mt-20 flex justify-center gap-10">
                    <div className="text-center">
                        <p className="text-5xl font-extrabold text-green-400">30%</p>
                        <p className="text-gray-400 mt-1">Time Saved</p>
                    </div>
                    <div className="text-center">
                        <p className="text-5xl font-extrabold text-green-400">40%</p>
                        <p className="text-gray-400 mt-1">Cost Reduction</p>
                    </div>
                </div>
            </div>
        </section>

        {/* 2. The Problem & Solution (Why AutoSchedule) */}
        <section id="problem-solution" className="mb-40 pt-10">
          <h2 className="font-pretendard text-5xl font-extrabold mb-14 text-center tracking-tight">
            The Problem & Our AI-Powered Solution
          </h2>
          
          <div className="flex flex-col md:flex-row justify-between gap-12 max-w-6xl mx-auto">
            {/* 좌측: 문제점 */}
            <div className="w-full md:w-1/2 p-8 bg-red-50 rounded-2xl shadow-md">
              <h3 className="text-3xl font-bold text-red-600 mb-6">❌ 기존 방식의 문제점</h3>
              <ul className="space-y-4 text-xl text-gray-700">
                <li className="flex items-start"><span className="text-red-500 mr-3">●</span> 수동 입력: 일정 등록에 드는 불필요한 시간 낭비</li>
                <li className="flex items-start"><span className="text-red-500 mr-3">●</span> 비효율적인 동기화: 여러 플랫폼에 수기로 옮겨 적는 번거로움</li>
                <li className="flex items-start"><span className="text-red-500 mr-3">●</span> 휴먼 에러: 날짜, 시간, 장소 오기로 인한 약속 누락</li>
              </ul>
            </div>
            
            {/* 우측: 해결책 */}
            <div className="w-full md:w-1/2 p-8 bg-blue-50 rounded-2xl shadow-md">
              <h3 className="text-3xl font-bold text-blue-600 mb-6">✅ AutoSchedule의 AI 솔루션</h3>
              <ul className="space-y-4 text-xl text-gray-700">
                <li className="flex items-start"><span className="text-blue-500 mr-3">●</span> 지능형 분석: 메모를 완벽하게 이해하고 일정을 추출</li>
                <li className="flex items-start"><span className="text-blue-500 mr-3">●</span> 전면 간소화: 수동 입력 최소화, 단 한 번의 확인으로 등록 완료</li>
                <li className="flex items-start"><span className="text-blue-500 mr-3">●</span> 통합 관리: 모든 캘린더와 플랫폼에 즉시 동기화</li>
              </ul>
            </div>
          </div>

          {/* 개발자 정보 (포트폴리오 강조) */}
          <div className="mt-16 text-center text-gray-600">
              <h3 className="font-pretendard text-3xl font-black mb-3">Developer: 하태영</h3>
              <p className="font-pretendard text-lg text-gray-700">본 프로젝트는 하태영 개발자의 백엔드 AI 분석 및 인프라 설계 역량을 중심으로 완성되었습니다.</p>
              <p className="font-pretendard text-md text-gray-500 mt-2">스마트IoT 전공 | Backend 개발 및 AI/NLP 엔지니어링 포커스</p>
          </div>
        </section>


        {/* 3. How Our AI Works - 이미지 추가된 부분 */}
        <section id="how-it-works" className="mb-40 pt-10">
          <h2 className="font-pretendard text-5xl font-extrabold mb-8 text-center tracking-tight">
            How AutoSchedule Works
          </h2>
          <p className="text-xl text-gray-600 text-center mb-20">단 세 단계로, 일정을 시간 자산으로 바꾸세요.</p>
          
          <div className="flex flex-col md:flex-row justify-between items-start gap-12 max-w-6xl mx-auto">
            {howItWorksSteps.map((step) => (
              <div key={step.step} className="flex-1 text-center p-6 bg-gray-50 rounded-xl shadow-lg transition duration-300 hover:shadow-xl">
                {/* 🚩 이미지 추가: public/images 폴더의 아이콘 사용 */}
                <img 
                    src={step.icon} 
                    alt={`Step ${step.step}`} 
                    className="h-20 object-contain mb-4 mx-auto block" 
                />
                <h3 
                    className="text-2xl font-extrabold mb-3 text-blue-600"
                    dangerouslySetInnerHTML={{ __html: step.title }}
                />
                <p className="text-gray-700 text-md mt-2">{step.description}</p>
              </div>
            ))}
          </div>
        </section>
        
        {/* 4. Demo & Key Features Section (미구현/시연 영역) */}
        <section id="features-demo" className="mb-40 pt-10">
            <h2 className="font-pretendard text-5xl font-extrabold mb-8 text-center tracking-tight">
                Demo: AutoSchedule의 핵심 기술
            </h2>
            <p className="text-xl text-gray-600 text-center mb-20">백엔드 AI/NLP 역량이 집중된, 세 가지 핵심 기능으로 시간을 관리하세요.</p>

            <div className="max-w-7xl mx-auto space-y-20">
                
                {/* 4-1. 시연 이미지/영상 자리 (미구현을 보여주는 플레이스홀더) */}
                {/* <div className="bg-gray-100 p-16 rounded-3xl shadow-2xl border-4 border-dashed border-gray-300 text-center">
                    <p className="text-3xl font-bold text-gray-500 mb-4">
                        [AI Demo Screen Capture / 서비스 작동 시연 영상 임베드 영역]
                    </p>
                    <a 
                        href="/schedule"
                        className="text-lg font-bold text-blue-600 hover:text-blue-800 transition duration-300 block mt-4"
                    >
                        실제 일정 등록 화면에서 기능 확인하기 →
                    </a>
                </div> */}
                
                {/* 4-2. 상세 기능 목록 */}
                <div className="grid md:grid-cols-3 gap-10">
                    {keyFeatures.map((feature, index) => (
                        <div key={index} className="p-8 border rounded-xl shadow-lg hover:shadow-xl transition duration-300 bg-white">
                            <div className={`w-12 h-12 flex items-center justify-center rounded-lg mb-4 ${feature.color}`}>
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={feature.iconSvgPath}></path>
                                </svg>
                            </div>
                            <h3 className="text-2xl font-bold mb-3 text-gray-800">{feature.title}</h3>
                            <p className="text-gray-600">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>


        {/* 5. Pricing Section - 🚩 기술 미구현으로 인해 해당 섹션 전체 제거 */}
        {/*
        <section id="pricing" className="mb-40 pt-10">
            ... (Pricing 섹션 내용 전체 삭제) ...
        </section>
        */}


        {/* 6. Contact Section (개인 연락처만 남김) */}
        <section id="contact" className="mb-40 max-w-3xl mx-auto pb-32">
          <h2 className="font-pretendard text-5xl font-extrabold mb-8 text-center">Contact Developer</h2>
          <p className="font-pretendard text-xl text-gray-700 text-center mb-10">기술 구현 관련 질문 및 포트폴리오 제안은 아래 연락처로 문의 주시기 바랍니다.</p>
          <div className="font-pretendard text-xl flex justify-center items-center gap-12 text-center">
            <p className="text-2xl font-bold text-gray-800">하태영: electro0218@gmail.com</p>
          </div>
        </section>

      </main>
    </div>
  );
};

export default MainPage;