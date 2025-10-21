/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";

export const TextareaField = ({
  hasLabel = true,
  hasError = false,
  label = "Label",
  error = "Hint",
  description = "Description",
  hasDescription = false,
  value = "Value",
  state,
  valueType,
  className,
  textareaClassName,
  dragClassName,
  drag = "https://c.animaapp.com/V2AgVb95/img/drag-1.svg",
}) => {
  return (
    <div
      className={`inline-flex flex-col items-start gap-[var(--size-space-200)] relative ${className}`}
    >
      {hasLabel && (
        <div className="relative self-stretch mt-[-1.00px] font-body-base font-[number:var(--body-base-font-weight)] text-color-text-default-default text-[length:var(--body-base-font-size)] tracking-[var(--body-base-letter-spacing)] leading-[var(--body-base-line-height)] [font-style:var(--body-base-font-style)]">
          {label}
        </div>
      )}

      <div
        className={`flex min-w-60 min-h-20 items-start pt-[var(--size-space-300)] pr-[var(--size-space-400)] pb-[var(--size-space-300)] pl-[var(--size-space-400)] relative self-stretch w-full flex-[0_0_auto] mb-[-1.00px] ml-[-1.00px] mr-[-1.00px] bg-color-background-default-default rounded-[var(--size-radius-200)] overflow-hidden border border-solid border-color-border-default-default ${textareaClassName}`}
      >
        <div className="relative flex-1 mt-[-0.50px] font-body-base font-[number:var(--body-base-font-weight)] text-color-text-default-default text-[length:var(--body-base-font-size)] tracking-[var(--body-base-letter-spacing)] leading-[var(--body-base-line-height)] [font-style:var(--body-base-font-style)]">
          {value}
        </div>

        <img
          className={`absolute w-[7px] h-[7px] top-[67px] left-[228px] ${dragClassName}`}
          alt="Drag"
          src={drag}
        />
      </div>
    </div>
  );
};
