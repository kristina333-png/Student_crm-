<template>
  <div class="home">
    <div class="hero">
      <h1>Student CRM</h1>
      <p class="subtitle">Система управления студентами, группами и оценками</p>
      <div class="actions">
        <router-link to="/students" class="btn-primary">Список студентов</router-link>
        <router-link to="/students/create" class="btn-secondary">Добавить студента</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
}
.hero {
  padding: 60px 20px;
}
.hero h1 {
  font-size: 3em;
  color: #2c3e50;
  margin-bottom: 10px;
}
.subtitle {
  font-size: 1.2em;
  color: #7f8c8d;
  margin-bottom: 40px;
}
.actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}
.btn-primary, .btn-secondary {
  padding: 14px 30px;
  border-radius: 10px;
  font-size: 1.1em;
  text-decoration: none;
  font-weight: 500;
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-primary {
  background: #3498db;
  color: white;
}
.btn-secondary {
  background: white;
  color: #3498db;
  border: 2px solid #3498db;
}
.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(52, 152, 219, 0.3);
}
</style>