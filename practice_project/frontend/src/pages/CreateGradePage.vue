<script setup>
import { useRouter } from "vue-router";
import GradeForm from "../components/GradeForm.vue";
import { createGrade } from "../api/grades";

const router = useRouter();

async function handleSubmit(data) {
  try {
    await createGrade(data);
    router.push("/grades");
  } catch (e) {
    alert("Ошибка: " + (e.response?.data?.detail || e.message));
  }
}
</script>

<template>
  <div>
    <h1>Добавить оценку</h1>
    <GradeForm @submit="handleSubmit" />
  </div>
</template>