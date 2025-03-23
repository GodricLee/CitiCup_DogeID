import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001',  // 后端 API 地址
  timeout: 5000, // 请求超时设置
});

export default api;
