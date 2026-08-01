```javascript
import axios from "axios";

const API = axios.create({
  baseURL: "https://teacher-ai-platform.onrender.com",
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await API.post("/upload/", formData);

  console.log("Upload response:", response.data);

  // Return ONLY the backend JSON
  return response.data;
};

export const processDocument = async (path) => {
  const response = await API.post("/process/", {
    path: path,
  });

  console.log("Process response:", response.data);

  // Return ONLY the backend JSON
  return response.data;
};

export default API;
```

