import axios from "axios";

const API = axios.create({
  baseURL: "import.meta.env.VITE_API_URL,
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
