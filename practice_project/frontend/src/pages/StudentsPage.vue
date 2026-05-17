<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { getStudents, deleteStudent } from "../api/students";
import { getGroups } from "../api/groups";

const router = useRouter();

const students = ref([]);
const groups = ref([]);
const loading = ref(true);
const error = ref(null);

const search = ref("");
const groupId = ref(null);
const currentPage = ref(1);
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

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">Ошибка: {{ error }}</div>

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
        <tr v-for="student in students" :key="student.id" @click="goToDetail(student.id)" style="cursor:pointer">
          <td>{{ student.id }}</td>
          <td>{{ student.first_name }}</td>
          <td>{{ student.last_name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.group_name || "—" }}</td>
          <td @click.stop>
            <button @click="goToEdit(student.id)">Редактировать</button>
            <button @click="handleDelete(student.id)">Удалить</button>
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
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}
.controls input {
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 200px;
}
.controls select {
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.btn-add {
  padding: 8px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-add:hover {
  background: #218838;
}
.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}
.pagination button {
  padding: 6px 12px;
  cursor: pointer;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
tr:hover {
  background-color: #f5f5f5;
}
</style>