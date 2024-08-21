import React from "react";

const ResultTable = ({ data }) => {
  console.log("res", data);
  const confidence = (parseFloat(data.confidence) * 100).toFixed(2);

  return (
    <div className="mt-4 border border-red-400">
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th className="px-4 py-2 text-left bg-blue-500 text-white">
              Label
            </th>
            <th className="px-4 py-2 text-right bg-blue-500 text-white">
              Confidence
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 bg-gray-700 text-white">
              {data.class}
            </td>
            <td className="border px-4 py-2 text-right bg-gray-700 text-white">
              {confidence}%
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default ResultTable;
