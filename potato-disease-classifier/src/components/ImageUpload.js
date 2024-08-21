import React, { useState, useEffect } from "react";
import axios from "axios";
import ClearButton from "./ClearButton";
import ResultTable from "./ResultTable";
import bg_farmer from "../bg_farmer.jpg";

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState();
  const [preview, setPreview] = useState();
  const [data, setData] = useState();
  const [image, setImage] = useState(false);
  const [isLoading, setIsloading] = useState(false);

  const sendFile = async () => {
    if (image) {
      let formData = new FormData();
      formData.append("file", selectedFile);
      let res = await axios.post("http://localhost:8001/predict", formData);

      if (res.status === 200) {
        setData(res.data);
      }
      setIsloading(false);
    }
  };

  const clearData = () => {
    setData(null);
    setImage(false);
    setSelectedFile(null);
    setPreview(null);
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    if (!preview) {
      return;
    }
    setIsloading(true);
    sendFile();
  }, [preview]);

  const onSelectFile = (files) => {
    if (!files || files.length === 0) {
      setSelectedFile(undefined);
      setImage(false);
      setData(undefined);
      return;
    }
    setSelectedFile(files[0]);
    setData(undefined);
    setImage(true);
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen bg-cover bg-center"
      style={{
        backgroundImage: `url(${bg_farmer})`,
      }}
    >

      <div className="max-w-sm w-full bg-white/20 backdrop-blur-lg p-4 rounded-lg shadow-lg">
        {!image && (
          <div className="p-6 text-center">
            <input
              type="file"
              accept="image/*"
              onChange={(e) => onSelectFile(e.target.files)}
            />
            <p className="mt-2 text-sm text-gray-700">
              Drag and drop an image of a potato plant leaf to process
            </p>
          </div>
        )}
        {image && (
          <div>
            <img
              src={preview}
              alt="Selected"
              className="w-full h-64 object-cover rounded-lg"
            />
          </div>
        )}
        {isLoading && (
          <div className="text-center mt-4">
            <div className="loader">Processing...</div>
          </div>
        )}
        {data && <ResultTable data={data} />}
        {data && <ClearButton clearData={clearData} />}
      </div>
    </div>
  );
};

export default ImageUpload;
