import axios from 'axios';

const API_BASE = '/api/v1';

export const checkHealth = async () => {
  const resp = await axios.get(`${API_BASE}/health`);
  return resp.data;
};

export const listStandards = async (params = {}) => {
  const resp = await axios.get(`${API_BASE}/standards`, { params });
  return resp.data;
};

export const getStandardsCount = async () => {
  const resp = await axios.get(`${API_BASE}/standards/count`);
  return resp.data.count;
};

export const getStandardDetail = async (id) => {
  const resp = await axios.get(`${API_BASE}/standards/${id}`);
  return resp.data;
};

export const validateStandard = async (isNumber) => {
  const resp = await axios.post(`${API_BASE}/standards/validate`, { is_number: isNumber });
  return resp.data;
};

export const extractRequirements = async (payload) => {
  const resp = await axios.post(`${API_BASE}/extract-requirements`, payload);
  return resp.data;
};

export const extractDocument = async (formData) => {
  const resp = await axios.post(`${API_BASE}/extract-document`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return resp.data;
};

export const analyzeTender = async (payload) => {
  const resp = await axios.post(`${API_BASE}/standards/analyze`, payload);
  return resp.data;
};

export const listAnalyses = async () => {
  const resp = await axios.get(`${API_BASE}/analyses`);
  return resp.data;
};

export const getAnalysisDetail = async (id) => {
  const resp = await axios.get(`${API_BASE}/analyses/${id}`);
  return resp.data;
};

export const getEvaluationMetrics = async () => {
  const resp = await axios.get(`${API_BASE}/evaluation`);
  return resp.data;
};

export const getBisStatus = async () => {
  const resp = await axios.get(`${API_BASE}/admin/status`);
  return resp.data;
};

export const triggerBisSync = async () => {
  const resp = await axios.post(`${API_BASE}/admin/standards/sync`);
  return resp.data;
};
