<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import GradeForm from "../components/GradeForm.vue";
import { getGrade, updateGrade } from "../api/grades";

const router = useRouter();
const route = useRoute();
const grade = ref(null);

onMounted(async () => {
  const res = await getGrade(route.params.id);
  grade.value = res.data;
});

async function handleSubmit(data) {
  try {
    await updateGrade(route.params.id, data);
    router.push("/grades");
  } catch (e) {
    alert("Ошибка: " + (e.response?.data?.detail || e.message));
  }
}
</script>

<template>
  <div>
    <h1>Редактировать оценку</h1>
    <GradeForm v-if="grade" :initialData="grade" :isEdit="true" @submit="handleSubmit" />
    <div v-else class="loader">Загрузка...</div>
  </div>
</template>