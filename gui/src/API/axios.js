import { default as axios } from "axios";
// Base URL for the api
const BASE_URL = "http://localhost:8000";

export default axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export { BASE_URL };
