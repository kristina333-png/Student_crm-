import apiClient from "./client";

export function getStudents(params = {}) {
  return apiClient.get("/students/", { params });
}

export function getStudent(id) {
  return apiClient.get(`/students/${id}`);
}

export function createStudent(data) {
  return apiClient.post("/students/", data);
}

export function updateStudent(id, data) {
  return apiClient.put(`/students/${id}`, data);
}

export function deleteStudent(id) {
  return apiClient.delete(`/students/${id}`);
}