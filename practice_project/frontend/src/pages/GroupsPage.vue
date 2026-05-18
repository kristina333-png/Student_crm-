<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getGroups, deleteGroup } from "../api/groups";

const router = useRouter();
const groups = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const limit = 10;
const total = ref(0);
const pages = ref(0);

const userRole = ref(localStorage.getItem("userRole") || "guest");

onMounted(() => loadGroups());

async function loadGroups() {
  loading.value = true;
  try {
    const params = { skip: (currentPage.value - 1) * limit, limit, sort_by: "id", order: "asc" };
    const res = await getGroups(params);
    groups.value = res.data.items;
    total.value = res.data.total;
    pages.value = res.data.pages;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

function goToPage(page) { currentPage.value = page; loadGroups(); }
function goToCreate() { router.push("/groups/create"); }
function goToEdit(id) { router.push(`/groups/${id}/edit`); }

async function handleDelete(id) {
  if (!confirm("Удалить группу?")) return;
  try { await deleteGroup(id); await loadGroups(); }
  catch (e) { alert("Ошибка: " + (e.response?.data?.detail || e.message)); }
}
</script>

<template>
  <div>
    <h1>Группы</h1>
    <button v-if="userRole === 'admin' || userRole === 'user'" class="btn-add" @click="goToCreate">+ Создать группу</button>

    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-else-if="error" class="error-msg">Ошибка: {{ error }}</div>

    <table v-else>
      <thead><tr><th>ID</th><th>Название</th><th>Описание</th><th>Студентов</th><th></th></tr></thead>
      <tbody>
        <tr v-for="group in groups" :key="group.id">
          <td>{{ group.id }}</td>
          <td>{{ group.name }}</td>
          <td>{{ group.description || "—" }}</td>
          <td>{{ group.student_count }}</td>
          <td class="actions-cell">
            <button v-if="userRole === 'admin' || userRole === 'teacher'" class="btn-icon" @click="goToEdit(student.id)">Редактировать</button>
            <button v-if="userRole === 'admin'" class="btn-icon" @click="handleDelete(group.id)">Удалить</button>
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
.btn-add { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 8px; font-size: 0.95em; cursor: pointer; margin-bottom: 20px; }
.btn-add:hover { background: #2980b9; }
.loader { text-align: center; padding: 40px; color: #95a5a6; }
.error-msg { background: #ffe6e6; color: #e74c3c; padding: 15px; border-radius: 8px; }
table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 15px rgba(0,0,0,0.05); }
th { background: #34495e; color: white; padding: 14px; text-align: left; }
td { padding: 12px 14px; border-bottom: 1px solid #eee; }
.actions-cell { white-space: nowrap; }
.btn-icon { background: none; border: none; font-size: 1.2em; cursor: pointer; padding: 4px 8px; border-radius: 6px; }
.btn-icon:hover { background: #eee; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 15px; margin-top: 20px; }
.pagination button { padding: 8px 16px; border: 2px solid #3498db; background: white; color: #3498db; border-radius: 8px; cursor: pointer; }
.pagination button:hover:not(:disabled) { background: #3498db; color: white; }
.pagination button:disabled { border-color: #ddd; color: #ccc; cursor: not-allowed; }
.pagination span { color: #7f8c8d; }
</style>