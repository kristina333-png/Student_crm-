<template>
  <div id="app">
    <header>
      <router-link to="/">Главная</router-link>
      <router-link to="/students">Студенты</router-link>
      <router-link to="/about">О проекте</router-link>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
header {
  display: flex;
  gap: 20px;
  padding: 10px;
  background: #f0f0f0;
}
header a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}
header a:hover {
  color: #007bff;
}
main {
  padding: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
</style>