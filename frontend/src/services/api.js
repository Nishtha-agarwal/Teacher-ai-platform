import axios from "axios";

const API = axios.create({
  baseURL: "https://teacher-ai-platform.onrender.com",
});

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/upload/", formData);
};

export const processDocument = (path) => {
  return API.post("/process/", {
    path: path,
  });
};

export default API;
