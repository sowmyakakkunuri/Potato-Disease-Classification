import React from "react";

const ClearButton = ({ clearData }) => {
  return (
    <div className="mt-4 text-center">
      <button
        onClick={clearData}
        className="px-4 py-2 bg-red-500 text-white font-bold rounded-full hover:bg-red-700"
      >
        Clear
      </button>
    </div>
  );
};

export default ClearButton;
