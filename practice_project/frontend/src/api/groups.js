import apiClient from "./client";

export function getGroups(params = {}) {
  return apiClient.get("/groups/", { params });
}

export function getGroup(id) {
  return apiClient.get(`/groups/${id}`);
}

export function createGroup(data) {
  return apiClient.post("/groups/", data);
}

export function updateGroup(id, data) {
  return apiClient.put(`/groups/${id}`, data);
}

export function deleteGroup(id) {
  return apiClient.delete(`/groups/${id}`);
}