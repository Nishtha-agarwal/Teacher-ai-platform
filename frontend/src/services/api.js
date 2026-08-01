import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

console.log("API URL:", API_URL);

const API = axios.create({
  baseURL: API_URL,
  timeout: 30000,
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  
  console.log("Uploading to:", `${API_URL}/upload/`);
  console.log("File:", file.name, file.type, file.size);
  
  return API.post("/upload/", formData);
  try {
    const response = await API.post("/upload/", formData);
    console.log("Upload response:", response.data);
    return response;
  } catch (error) {
    console.error("Upload error:", error);
    console.error("Request URL:", error.config?.baseURL + error.config?.url);
    console.error("Response:", error.response);
    console.error("Message:", error.message);
    throw error;
  }
};

export const processDocument = async (path) => {
  return API.post("/process/", {
    path: path,
  });
};

export default API;
