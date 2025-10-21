import React,{useState} from "react";
import { HashLink } from 'react-router-hash-link';
import { Rectangle } from "../../components/Rectangle";
import NavBar from "../../components/FixedNavBar";

const Memo = () => {
  const [memo1, setMemo1] = useState("");
  const [memo2, setMemo2] = useState("");

  return (
    <div className="bg-[#F1F1F1] min-h-screen flex flex-col items-center">
      <NavBar />
      <div className="pt-[180px] w-full max-w-7xl mx-auto">
        {/* 타이틀 */}
        <h2 className="text-4xl font-bold text-gray-900 text-center mb-10 tracking-tight">Memo</h2>

        {/* 메모장 두 칸 영역 */}
        <div className="flex flex-row justify-center gap-16">
          {/* 왼쪽 메모장 */}
          <div className="bg-white shadow-2xl rounded-2xl w-[420px] p-8 flex flex-col">
            <label className="text-xl font-semibold text-gray-700 mb-3">내 일정</label>
            <textarea
              className="border border-gray-200 rounded-lg p-4 resize-none min-h-[170px] text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              placeholder="일정을 입력하세요..."
              value={memo1}
              onChange={e => setMemo1(e.target.value)}
            />
            <button className="mt-6 py-3 w-full bg-indigo-600 text-white font-bold rounded-md shadow-md hover:bg-indigo-700 transition">
              일정 확인
            </button>
          </div>

          {/* 오른쪽 메모장 */}
          <div className="bg-white shadow-2xl rounded-2xl w-[420px] p-8 flex flex-col">
            <label className="text-xl font-semibold text-gray-700 mb-3">구글 캘린더 메모</label>
            <textarea
              className="border border-gray-200 rounded-lg p-4 resize-none min-h-[170px] text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              placeholder="구글 캘린더에 저장할 내용을 입력하세요..."
              value={memo2}
              onChange={e => setMemo2(e.target.value)}
            />
            <button className="mt-6 py-3 w-full bg-green-600 text-white font-bold rounded-md shadow-md hover:bg-green-700 transition">
              구글 캘린더에 저장
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Memo;