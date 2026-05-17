<script setup>
import { ref } from "vue";

const props = defineProps({
  initialData: { type: Object, default: () => ({}) },
  isEdit: { type: Boolean, default: false },
});

const emit = defineEmits(["submit"]);

const form = ref({
  first_name: props.initialData.first_name || "",
  last_name: props.initialData.last_name || "",
  email: props.initialData.email || "",
  phone: props.initialData.phone || "",
  group_id: props.initialData.group_id || "",
  enrollment_date: props.initialData.enrollment_date || "",
});

const error = ref(null);

function handleSubmit() {
  if (!form.value.first_name || !form.value.last_name || !form.value.email) {
    error.value = "Заполните обязательные поля: имя, фамилия, email";
    return;
  }

  const data = {
    first_name: form.value.first_name,
    last_name: form.value.last_name,
    email: form.value.email,
  };

  if (form.value.phone) data.phone = form.value.phone;
  if (form.value.group_id) data.group_id = Number(form.value.group_id);
  if (form.value.enrollment_date) data.enrollment_date = form.value.enrollment_date;

  emit("submit", data);
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="student-form">
    <div v-if="error" class="error">{{ error }}</div>

    <label>
      Имя *
      <input v-model="form.first_name" type="text" required />
    </label>

    <label>
      Фамилия *
      <input v-model="form.last_name" type="text" required />
    </label>

    <label>
      Email *
      <input v-model="form.email" type="email" required />
    </label>

    <label>
      Телефон
      <input v-model="form.phone" type="text" />
    </label>

    <label>
      Группа (ID)
      <input v-model="form.group_id" type="number" />
    </label>

    <label>
      Дата зачисления
      <input v-model="form.enrollment_date" type="date" />
    </label>

    <button type="submit">{{ isEdit ? "Обновить" : "Создать" }}</button>
  </form>
</template>

<style scoped>
.student-form {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
label {
  display: flex;
  flex-direction: column;
  font-weight: 500;
  color: #2c3e50;
  gap: 4px;
}
input {
  padding: 10px 14px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 0.95em;
  transition: border-color 0.3s;
}
input:focus {
  border-color: #3498db;
  outline: none;
}
button {
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 10px;
}
button:hover {
  background: #2980b9;
}
.error {
  background: #ffe6e6;
  color: #e74c3c;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e74c3c;
}
</style>