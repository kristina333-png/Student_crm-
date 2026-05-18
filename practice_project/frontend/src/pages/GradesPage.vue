<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { getGrades, deleteGrade } from "../api/grades";
import { getStudents } from "../api/students";

const router = useRouter();
const grades = ref([]);
const students = ref([]);
const loading = ref(true);
const error = ref(null);
const filterStudentId = ref(null);
const globalSearch = ref("");
const currentPage = ref(1);
const limit = 10;
const total = ref(0);
const pages = ref(0);

const userRole = ref(localStorage.getItem("userRole") || "guest");

let searchTimeout = null;

onMounted(() => { loadStudents(); loadGrades(); });

watch(globalSearch, () => {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
    loadGrades();
  }, 500);
});

watch(filterStudentId, () => {
  currentPage.value = 1;
  loadGrades();
});

async function loadStudents() {
  const res = await getStudents({ limit: 100 });
  students.value = res.data.items;
}

async function loadGrades() {
  loading.value = true;
  try {
    const searchTerm = globalSearch.value.toLowerCase().trim();

    // Определяем, искать по студенту или по предмету
    let studentIds = null;
    let subjectSearch = null;

    if (searchTerm) {
      // Ищем студентов по имени
      const matchedStudents = students.value.filter(s =>
        s.first_name.toLowerCase().includes(searchTerm) ||
        s.last_name.toLowerCase().includes(searchTerm)
      );
      studentIds = matchedStudents.map(s => s.id);

      // Если есть точное совпадение с предметом
      subjectSearch = searchTerm;
    }

    const params = {
      skip: (currentPage.value - 1) * limit,
      limit,
      sort_by: "id",
      order: "asc"
    };

    if (filterStudentId.value) params.student_id = filterStudentId.value;

    // Если нашли студентов по имени и нет фильтра по студенту
    if (studentIds && studentIds.length > 0 && !filterStudentId.value) {
      params.student_id = studentIds;
    }

    // Поиск по предмету
    if (subjectSearch) params.subject = subjectSearch;

    const res = await getGrades(params);
    let items = res.data.items;

    // Дополнительная фильтрация на клиенте
    if (searchTerm && !filterStudentId.value) {
      items = items.filter(g => {
        const student = students.value.find(s => s.id === g.student_id);
        const studentName = student ? `${student.first_name} ${student.last_name}`.toLowerCase() : "";
        const matchesStudent = studentName.includes(searchTerm);
        const matchesSubject = g.subject.toLowerCase().includes(searchTerm);
        return matchesStudent || matchesSubject;
      });
    }

    grades.value = items;
    total.value = items.length;
    pages.value = Math.ceil(total.value / limit);
  } catch (e) {
    error.value = e.message;
  }
  finally { loading.value = false; }
}

function goToPage(page) { currentPage.value = page; loadGrades(); }
function goToCreate() { router.push("/grades/create"); }
function goToEdit(id) { router.push(`/grades/${id}/edit`); }

async function handleDelete(id) {
  if (!confirm("Удалить оценку?")) return;
  try { await deleteGrade(id); await loadGrades(); }
  catch (e) { alert("Ошибка: " + (e.response?.data?.detail || e.message)); }
}

function getStudentName(studentId) {
  const s = students.value.find(st => st.id === studentId);
  return s ? `${s.first_name} ${s.last_name}` : `ID: ${studentId}`;
}
</script>

<template>
  <div>
    <h1>Оценки</h1>

    <div class="controls">
      <div class="search-wrapper">
        <input
          v-model="globalSearch"
          type="text"
          placeholder="Поиск по студенту или предмету..."
          class="search-input"
        />
        <button v-if="globalSearch" class="clear-search" @click="globalSearch = ''">✖</button>
      </div>
      <select v-model="filterStudentId">
        <option :value="null">Все студенты</option>
        <option v-for="s in students" :key="s.id" :value="s.id">{{ s.first_name }} {{ s.last_name }}</option>
      </select>
      <button v-if="userRole === 'admin' || userRole === 'user'" class="btn-add" @click="goToCreate">+ Добавить оценку</button>
    </div>

    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-else-if="error" class="error-msg">Ошибка: {{ error }}</div>

    <table v-else>
      <thead>
        <tr><th>ID</th><th>Студент</th><th>Предмет</th><th>Оценка</th><th>Дата</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="grade in grades" :key="grade.id">
          <td>{{ grade.id }}</td>
          <td>{{ getStudentName(grade.student_id) }}</td>
          <td>{{ grade.subject }}</td>
          <td>{{ grade.score }}</td>
          <td>{{ grade.grade_date || "—" }}</td>
          <td class="actions-cell">
            <button v-if="userRole === 'admin' || userRole === 'teacher'" class="btn-icon" @click="goToEdit(student.id)">Редактировать</button>
            <button v-if="userRole === 'admin'" class="btn-icon" @click="handleDelete(grade.id)">Удалить</button>
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
.controls { display: flex; gap: 12px; margin-bottom: 20px; align-items: center; flex-wrap: wrap; }
.search-wrapper { position: relative; }
.search-input { padding: 10px 14px; border: 2px solid #ddd; border-radius: 8px; font-size: 0.95em; width: 280px; }
.search-input:focus { border-color: #3498db; outline: none; }
.clear-search { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 1.1em; color: #999; }
.clear-search:hover { color: #e74c3c; }
.controls select { padding: 10px 14px; border: 2px solid #ddd; border-radius: 8px; font-size: 0.95em; }
.btn-add { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 8px; cursor: pointer; }
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