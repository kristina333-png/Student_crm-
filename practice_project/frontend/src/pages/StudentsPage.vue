<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getStudents, deleteStudent } from "../api/students";

const router = useRouter();
const students = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(() => loadStudents());

async function loadStudents() {
  loading.value = true;
  try {
    const response = await getStudents({ limit: 100 });
    students.value = response.data.items;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

function goToCreate() {
  router.push("/students/create");
}

function goToEdit(id) {
  router.push(`/students/${id}/edit`);
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
    <button class="btn-add" @click="goToCreate">+ Создать студента</button>

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
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.id }}</td>
          <td>{{ student.first_name }}</td>
          <td>{{ student.last_name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.group_name || "—" }}</td>
          <td>
            <button @click="goToEdit(student.id)">✏️</button>
            <button @click="handleDelete(student.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.btn-add {
  margin-bottom: 10px;
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
button {
  margin: 0 4px;
  cursor: pointer;
}
</style>