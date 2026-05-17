<script setup>
import { useRouter } from "vue-router";
import StudentForm from "../components/StudentForm.vue";
import { createStudent } from "../api/students";

const router = useRouter();

async function handleSubmit(data) {
  console.log("Отправляю:", JSON.stringify(data));
  try {
    const response = await createStudent(data);
    console.log("Успех:", response.data);
    router.push("/students");
  } catch (e) {
    console.error("Ошибка ответа:", e.response?.status, e.response?.data);
    alert("Ошибка: " + JSON.stringify(e.response?.data?.detail));
  }
}
</script>

<template>
  <div>
    <h1>Создать студента</h1>
    <StudentForm @submit="handleSubmit" />
  </div>
</template>