<script setup>
import { ref } from "vue";

const props = defineProps({
  initialData: { type: Object, default: () => ({}) },
  isEdit: { type: Boolean, default: false },
});

const emit = defineEmits(["submit"]);

const form = ref({
  name: props.initialData.name || "",
  description: props.initialData.description || "",
});

const error = ref(null);

function handleSubmit() {
  if (!form.value.name) {
    error.value = "Заполните название группы";
    return;
  }
  emit("submit", { ...form.value });
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="group-form">
    <div v-if="error" class="error">{{ error }}</div>
    <label>Название *<input v-model="form.name" type="text" required /></label>
    <label>Описание<textarea v-model="form.description" rows="3"></textarea></label>
    <button type="submit">{{ isEdit ? "Обновить" : "Создать" }}</button>
  </form>
</template>

<style scoped>
.group-form { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 15px rgba(0,0,0,0.05); max-width: 500px; display: flex; flex-direction: column; gap: 15px; }
label { display: flex; flex-direction: column; font-weight: 500; color: #2c3e50; gap: 4px; }
input, textarea { padding: 10px; border: 2px solid #ddd; border-radius: 8px; font-size: 0.95em; }
input:focus, textarea:focus { border-color: #3498db; outline: none; }
button { padding: 12px 24px; background: #3498db; color: white; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; }
button:hover { background: #2980b9; }
.error { background: #ffe6e6; color: #e74c3c; padding: 12px; border-radius: 8px; border: 1px solid #e74c3c; }
</style>