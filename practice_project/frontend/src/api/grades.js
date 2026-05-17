import apiClient from "./client";

export function getGrades(params = {}) {
  return apiClient.get("/grades/", { params });
}

export function getGrade(id) {
  return apiClient.get(`/grades/${id}`);
}

export function createGrade(data) {
  return apiClient.post("/grades/", data);
}

export function updateGrade(id, data) {
  return apiClient.put(`/grades/${id}`, data);
}

export function deleteGrade(id) {
  return apiClient.delete(`/grades/${id}`);
}