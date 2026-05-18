<template>
  <div id="app">
    <header v-if="isLoggedIn">
      <div class="logo">Student CRM</div>
      <nav>
        <router-link to="/">Главная</router-link>
        <router-link to="/students">Студенты</router-link>
        <router-link to="/grades">Оценки</router-link>
        <router-link to="/groups">Группы</router-link>
        <router-link v-if="userRole === 'admin'" to="/register">Регистрация</router-link>
        <router-link to="/about">О проекте</router-link>
        <button class="logout-btn" @click="logout">Выйти</button>
      </nav>
    </header>
    <header v-else class="simple-header">
      <div class="logo">Student CRM</div>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>© 2026 Student CRM — учебный проект</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const isLoggedIn = ref(false);
const userRole = ref("");

function checkAuth() {
  isLoggedIn.value = !!localStorage.getItem("accessToken");
  userRole.value = localStorage.getItem("userRole") || "";
}

function logout() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("userRole");
  localStorage.removeItem("userName");
  localStorage.removeItem("userId");
  checkAuth();
  router.push("/login");
}

onMounted(() => {
  checkAuth();
  watch(() => route.path, () => {
    checkAuth();
  });
});
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f4f6f9;
  color: #333;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background: #2c3e50;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.simple-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px 30px;
  background: #2c3e50;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.5em;
  font-weight: bold;
}

nav {
  display: flex;
  gap: 25px;
  align-items: center;
}

nav a {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

nav a:hover {
  color: #3498db;
}

nav a.router-link-exact-active {
  color: #3498db;
}

.logout-btn {
  background: none;
  border: none;
  color: #e74c3c;
  font-weight: 500;
  cursor: pointer;
  font-size: 1em;
  font-family: inherit;
  padding: 0;
  transition: color 0.3s;
}

.logout-btn:hover {
  color: #c0392b;
}

main {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}

footer {
  text-align: center;
  padding: 20px;
  color: #95a5a6;
  font-size: 0.9em;
  margin-top: 50px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.8em;
}
</style>