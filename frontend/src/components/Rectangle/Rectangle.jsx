/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { TextareaField } from "../TextareaField";

export const Rectangle = ({ className }) => {
  return (
    <div className={`w-[568px] h-[281px] ${className}`}>
      <div className="relative w-[676px] h-[507px] top-[125px] left-[-25px] bg-[url(https://c.animaapp.com/V2AgVb95/img/rectangle-2-2.svg)] bg-[100%_100%]">
        <TextareaField
          className="!h-[381px] !flex !left-11 !w-[589px] !top-[39px]"
          drag="https://c.animaapp.com/V2AgVb95/img/drag-3.svg"
          dragClassName="!left-[577px] !top-[338px]"
          label="제목 작성"
          state="default"
          textareaClassName="!flex-1 !bg-white !grow"
          value="일정을 기록하세요..."
          valueType="default"
        />
      </div>
    </div>
  );
};
