<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import GroupForm from "../components/GroupForm.vue";
import { getGroup, updateGroup } from "../api/groups";

const router = useRouter();
const route = useRoute();
const group = ref(null);

onMounted(async () => {
  const res = await getGroup(route.params.id);
  group.value = res.data;
});

async function handleSubmit(data) {
  try {
    await updateGroup(route.params.id, data);
    router.push("/groups");
  } catch (e) {
    alert("Ошибка: " + (e.response?.data?.detail || e.message));
  }
}
</script>

<template>
  <div>
    <h1>Редактировать группу</h1>
    <GroupForm v-if="group" :initialData="group" :isEdit="true" @submit="handleSubmit" />
    <div v-else class="loader">Загрузка...</div>
  </div>
</template>