<template>
  <div id="app">
    <header>
      <div class="logo">Student CRM</div>
      <nav>
        <router-link to="/">Главная</router-link>
        <router-link to="/students">Студенты</router-link>
        <router-link to="/about">О проекте</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>© 2026 Student CRM — учебный проект</p>
    </footer>
  </div>
</template>

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

.logo {
  font-size: 1.5em;
  font-weight: bold;
}

nav {
  display: flex;
  gap: 25px;
}

nav a {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

nav a:hover, nav a.router-link-exact-active {
  color: #3498db;
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