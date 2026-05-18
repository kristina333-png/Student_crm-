<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import apiClient from "../api/client";

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref(null);

async function login() {
  error.value = null;
  try {
    const res = await apiClient.post("/auth_jwt/login", {
      username: username.value,
      password: password.value,
    });

    // Сохраняем токен и данные пользователя
    localStorage.setItem("accessToken", res.data.access_token);
    localStorage.setItem("userRole", res.data.user.role);
    localStorage.setItem("userName", res.data.user.full_name);
    localStorage.setItem("userId", res.data.user.id);

    router.push("/students");
  } catch (e) {
    error.value = e.response?.data?.detail || "Ошибка входа";
  }
}
</script>

<template>
  <div class="login">
    <div class="login-card">
      <h1>Student CRM</h1>
      <p>Войдите в систему</p>

      <div v-if="error" class="error">{{ error }}</div>

      <label>Логин
        <input v-model="username" type="text" />
      </label>

      <label>Пароль
        <input v-model="password" type="password" />
      </label>

      <button class="btn-login" @click="login">Войти</button>
    </div>
  </div>
</template>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
.login-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 5px 30px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}
.login-card h1 { margin-bottom: 5px; }
.login-card p { color: #7f8c8d; margin-bottom: 20px; }
label { display: flex; flex-direction: column; text-align: left; font-weight: 500; color: #2c3e50; gap: 4px; margin-bottom: 15px; }
input { padding: 10px; border: 2px solid #ddd; border-radius: 8px; font-size: 1em; }
input:focus { border-color: #3498db; outline: none; }
.btn-login { padding: 14px; background: #3498db; color: white; border: none; border-radius: 10px; font-size: 1.1em; cursor: pointer; width: 100%; margin-top: 10px; }
.btn-login:hover { background: #2980b9; }
.error { background: #ffe6e6; color: #e74c3c; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
.hint { margin-top: 20px; text-align: left; font-size: 0.85em; color: #95a5a6; line-height: 1.6; }
.hint strong { color: #7f8c8d; }
</style>