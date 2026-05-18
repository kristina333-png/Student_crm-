<script setup>
import { useRouter } from "vue-router";
import GroupForm from "../components/GroupForm.vue";
import { createGroup } from "../api/groups";

const router = useRouter();

async function handleSubmit(data) {
  try {
    await createGroup(data);
    router.push("/groups");
  } catch (e) {
    alert("Ошибка: " + (e.response?.data?.detail || e.message));
  }
}
</script>

<template>
  <div>
    <h1>Создать группу</h1>
    <GroupForm @submit="handleSubmit" />
  </div>
</template>