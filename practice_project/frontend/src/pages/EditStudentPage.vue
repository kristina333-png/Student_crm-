<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import StudentForm from "../components/StudentForm.vue";
import { getStudent, updateStudent } from "../api/students";

const router = useRouter();
const route = useRoute();
const student = ref(null);

onMounted(async () => {
  try {
    const response = await getStudent(route.params.id);
    student.value = response.data;
  } catch (e) {
    alert("Ошибка загрузки студента");
    router.push("/students");
  }
});

async function handleSubmit(data) {
  try {
    await updateStudent(route.params.id, data);
    router.push("/students");
  } catch (e) {
    alert("Ошибка: " + (e.response?.data?.detail || e.message));
  }
}
</script>

<template>
  <div>
    <h1>Редактировать студента</h1>
    <StudentForm v-if="student" :initialData="student" :isEdit="true" @submit="handleSubmit" />
    <div v-else>Загрузка...</div>
  </div>
</template>