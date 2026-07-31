import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export async function uploadFile(file) {

  const formData = new FormData();

  formData.append("file", file);

  const res = await API.post(
    "/upload/",
    formData
  );

  return res.data;
}


export async function processDocument(path) {

  const res = await API.post(
    "/process/",
    {
      path
    }
  );

  return res.data;
}