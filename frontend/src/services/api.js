import axios from "axios";

const API = axios.create({
  baseURL: "https://teacher-ai-platform.onrender.com",
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await API.post("/upload/", formData);

  console.log("=== UPLOAD API ===");
  console.log("Axios response:", response);
  console.log("Response data:", response.data);
  console.log("Response path:", response.data?.path);

  return response.data;
};

export const processDocument = async (path) => {
  console.log("=== PROCESS API ===");
  console.log("Sending path:", path);

  const response = await API.post("/process/", {
    path: path,
  });

  console.log("Process response:", response);
  console.log("Process data:", response.data);

  return response.data;
};

export default API;

