import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const queryMedicalBot = async (question) => {
  const response = await API.get("/query", {
    params: { question },
  });
  return response.data;
};
