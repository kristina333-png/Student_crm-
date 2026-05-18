<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import apiClient from "../api/client";

const router = useRouter();
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const fullName = ref("");
const role = ref("student");
const error = ref(null);
const success = ref(null);

async function register() {
  error.value = null;
  success.value = null;

  if (!username.value || !password.value || !fullName.value) {
    error.value = "Заполните все обязательные поля";
    return;
  }

  if (password.value !== confirmPassword.value) {
    error.value = "Пароли не совпадают";
    return;
  }

  if (password.value.length < 4) {
    error.value = "Пароль должен быть не менее 4 символов";
    return;
  }

  try {
    await apiClient.post("/auth_jwt/register", {
      username: username.value,
      password: password.value,
      full_name: fullName.value,
      role: role.value,
    });
    success.value = "Пользователь успешно создан!";
    setTimeout(() => {
      router.push("/students");
    }, 1500);
  } catch (e) {
    error.value = e.response?.data?.detail || "Ошибка регистрации";
  }
}
</script>

<template>
  <div class="register">
    <div class="register-card">
      <h1>Регистрация пользователя</h1>
      <p>Создание нового аккаунта</p>

      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>

      <label>Логин *
        <input v-model="username" type="text" placeholder="username" />
      </label>

      <label>Полное имя *
        <input v-model="fullName" type="text" placeholder="Иван Иванов" />
      </label>

      <label>Пароль *
        <input v-model="password" type="password" placeholder="****" />
      </label>

      <label>Подтверждение пароля *
        <input v-model="confirmPassword" type="password" placeholder="****" />
      </label>

      <label>Роль
        <select v-model="role">
          <option value="teacher">Учитель</option>
          <option value="student">Студент</option>
        </select>
      </label>

      <button class="btn-register" @click="register">Зарегистрировать</button>
      <button class="btn-back" @click="router.push('/students')">Назад</button>
    </div>
  </div>
</template>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}
.register-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 5px 30px rgba(0,0,0,0.1);
  max-width: 450px;
  width: 100%;
}
.register-card h1 { margin-bottom: 5px; font-size: 1.5em; }
.register-card p { color: #7f8c8d; margin-bottom: 20px; }
label { display: flex; flex-direction: column; text-align: left; font-weight: 500; color: #2c3e50; gap: 4px; margin-bottom: 15px; }
input, select { padding: 10px; border: 2px solid #ddd; border-radius: 8px; font-size: 1em; }
input:focus, select:focus { border-color: #3498db; outline: none; }
.btn-register { padding: 12px; background: #27ae60; color: white; border: none; border-radius: 10px; font-size: 1em; cursor: pointer; width: 100%; margin-bottom: 10px; }
.btn-register:hover { background: #219a52; }
.btn-back { padding: 12px; background: #95a5a6; color: white; border: none; border-radius: 10px; font-size: 1em; cursor: pointer; width: 100%; }
.btn-back:hover { background: #7f8c8d; }
.error { background: #ffe6e6; color: #e74c3c; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
.success { background: #e6ffe6; color: #27ae60; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
</style>