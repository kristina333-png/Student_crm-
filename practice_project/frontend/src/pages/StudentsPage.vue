<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { getStudents, deleteStudent } from "../api/students";
import { getGroups } from "../api/groups";

const router = useRouter();
const route = useRoute();

const students = ref([]);
const groups = ref([]);
const loading = ref(true);
const error = ref(null);

const search = ref(route.query.search || "");
const groupId = ref(route.query.group_id ? Number(route.query.group_id) : null);
const currentPage = ref(Number(route.query.page) || 1);
const limit = 10;
const total = ref(0);
const pages = ref(0);

onMounted(() => {
  loadGroups();
  loadStudents();
});

async function loadGroups() {
  try {
    const res = await getGroups({ limit: 100 });
    groups.value = res.data.items;
  } catch (e) {}
}

async function loadStudents() {
  loading.value = true;
  try {
    const params = {
      skip: (currentPage.value - 1) * limit,
      limit: limit,
      sort_by: "id",
      order: "asc",
    };
    if (search.value) params.search = search.value;
    if (groupId.value) params.group_id = groupId.value;

    const query = { page: currentPage.value };
    if (search.value) query.search = search.value;
    if (groupId.value) query.group_id = groupId.value;
    router.replace({ query });

    const res = await getStudents(params);
    students.value = res.data.items;
    total.value = res.data.total;
    pages.value = res.data.pages;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

watch([search, groupId], () => {
  currentPage.value = 1;
  loadStudents();
});

function goToPage(page) {
  currentPage.value = page;
  loadStudents();
}

function goToCreate() {
  router.push("/students/create");
}

function goToEdit(id) {
  router.push(`/students/${id}/edit`);
}

function goToDetail(id) {
  router.push(`/students/${id}`);
}

async function handleDelete(id) {
  if (!confirm("Удалить студента?")) return;
  try {
    await deleteStudent(id);
    await loadStudents();
  } catch (e) {
    alert("Ошибка: " + (e.response?.data?.detail || e.message));
  }
}
</script>

<template>
  <div>
    <h1>Студенты</h1>

    <div class="controls">
      <input v-model="search" placeholder="Поиск по имени или email..." @keyup.enter="loadStudents" />
      <select v-model="groupId">
        <option :value="null">Все группы</option>
        <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
      </select>
      <button class="btn-add" @click="goToCreate">+ Создать</button>
    </div>

    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-else-if="error" class="error-msg">Ошибка: {{ error }}</div>

    <table v-else>
      <thead>
        <tr>
          <th>ID</th>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Email</th>
          <th>Группа</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id" @click="goToDetail(student.id)" class="clickable">
          <td>{{ student.id }}</td>
          <td>{{ student.first_name }}</td>
          <td>{{ student.last_name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.group_name || "—" }}</td>
          <td @click.stop class="actions-cell">
            <button class="btn-icon" @click="goToEdit(student.id)" title="Редактировать">Редактировать</button>
            <button class="btn-icon" @click="handleDelete(student.id)" title="Удалить">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="pages > 1" class="pagination">
      <button :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">← Назад</button>
      <span>Стр. {{ currentPage }} из {{ pages }} (всего: {{ total }})</span>
      <button :disabled="currentPage === pages" @click="goToPage(currentPage + 1)">Вперёд →</button>
    </div>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}
.controls input, .controls select {
  padding: 10px 14px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 0.95em;
  transition: border-color 0.3s;
}
.controls input:focus, .controls select:focus {
  border-color: #3498db;
  outline: none;
}
.controls input {
  width: 250px;
}
.btn-add {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95em;
  cursor: pointer;
  transition: background 0.3s;
}
.btn-add:hover {
  background: #2980b9;
}
.loader {
  text-align: center;
  padding: 40px;
  color: #95a5a6;
  font-size: 1.1em;
}
.error-msg {
  background: #ffe6e6;
  color: #e74c3c;
  padding: 15px;
  border-radius: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}
th {
  background: #34495e;
  color: white;
  padding: 14px;
  text-align: left;
  font-weight: 500;
}
td {
  padding: 12px 14px;
  border-bottom: 1px solid #eee;
}
.clickable {
  cursor: pointer;
}
.clickable:hover {
  background: #f8fafc;
}
.actions-cell {
  white-space: nowrap;
}
.btn-icon {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}
.btn-icon:hover {
  background: #eee;
}
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}
.pagination button {
  padding: 8px 16px;
  border: 2px solid #3498db;
  background: white;
  color: #3498db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}
.pagination button:hover:not(:disabled) {
  background: #3498db;
  color: white;
}
.pagination button:disabled {
  border-color: #ddd;
  color: #ccc;
  cursor: not-allowed;
}
.pagination span {
  color: #7f8c8d;
}
</style>