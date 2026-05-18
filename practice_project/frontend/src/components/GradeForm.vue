<script setup>
import { ref, onMounted } from "vue";
import { getStudents } from "../api/students";

const props = defineProps({
  initialData: { type: Object, default: () => ({}) },
  isEdit: { type: Boolean, default: false },
});

const emit = defineEmits(["submit"]);

const students = ref([]);

const form = ref({
  student_id: props.initialData.student_id || "",
  subject: props.initialData.subject || "",
  score: props.initialData.score || "",
  grade_date: props.initialData.grade_date || "",
});

const error = ref(null);

onMounted(async () => {
  const res = await getStudents({ limit: 100 });
  students.value = res.data.items;
});

function handleSubmit() {
  if (!form.value.student_id || !form.value.subject || !form.value.score) {
    error.value = "Заполните обязательные поля";
    return;
  }
  emit("submit", {
    student_id: Number(form.value.student_id),
    subject: form.value.subject,
    score: Number(form.value.score),
    grade_date: form.value.grade_date || null,
  });
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="grade-form">
    <div v-if="error" class="error">{{ error }}</div>

    <label>Студент *
      <select v-model="form.student_id">
        <option value="">Выберите студента</option>
        <option v-for="s in students" :key="s.id" :value="s.id">{{ s.first_name }} {{ s.last_name }}</option>
      </select>
    </label>

    <label>Предмет *<input v-model="form.subject" type="text" required /></label>
    <label>Оценка *<input v-model="form.score" type="number" min="1" max="5" step="0.1" required /></label>
    <label>Дата<input v-model="form.grade_date" type="date" /></label>

    <button type="submit">{{ isEdit ? "Обновить" : "Создать" }}</button>
  </form>
</template>

<style scoped>
.grade-form { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 15px rgba(0,0,0,0.05); max-width: 500px; display: flex; flex-direction: column; gap: 15px; }
label { display: flex; flex-direction: column; font-weight: 500; color: #2c3e50; gap: 4px; }
input, select { padding: 10px; border: 2px solid #ddd; border-radius: 8px; font-size: 0.95em; }
input:focus, select:focus { border-color: #3498db; outline: none; }
button { padding: 12px 24px; background: #3498db; color: white; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; margin-top: 10px; }
button:hover { background: #2980b9; }
.error { background: #ffe6e6; color: #e74c3c; padding: 12px; border-radius: 8px; border: 1px solid #e74c3c; }
</style>