import axios from "axios";

const API = axios.create({
  baseURL: "https://teacher-ai-platform.onrender.com",
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await API.post("/upload/", formData);

  console.log("RAW AXIOS RESPONSE:", response);
  console.log("UPLOAD DATA:", response.data);
  console.log("UPLOAD PATH:", response.data?.path);

  return response.data;
};

export const processDocument = async (path) => {
  const response = await API.post("/process/", {
    path: path,
  });
  
  console.log("RAW PROCESS RESPONSE:", response);
  console.log("PROCESS DATA:", response.data);

  return response.data;
};

export default API;

