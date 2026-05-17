<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getStudent } from "../api/students";
import apiClient from "../api/client";

const route = useRoute();
const student = ref(null);
const comments = ref([]);
const newAuthor = ref("");
const newText = ref("");

onMounted(async () => {
  const res = await getStudent(route.params.id);
  student.value = res.data;
  loadComments();
});

async function loadComments() {
  const res = await apiClient.get(`/students/${route.params.id}/comments/`);
  comments.value = res.data;
}

async function addComment() {
  if (!newAuthor.value || !newText.value) return;
  await apiClient.post(`/students/${route.params.id}/comments/`, {
    author_name: newAuthor.value,
    text: newText.value,
  });
  newAuthor.value = "";
  newText.value = "";
  await loadComments();
}

async function deleteComment(commentId) {
  await apiClient.delete(`/students/${route.params.id}/comments/${commentId}`);
  await loadComments();
}
</script>

<template>
  <div v-if="student" class="detail">
    <h1>{{ student.first_name }} {{ student.last_name }}</h1>

    <div class="info-card">
      <p><strong>Email:</strong> {{ student.email }}</p>
      <p><strong>Телефон:</strong> {{ student.phone || "—" }}</p>
      <p><strong>Группа:</strong> {{ student.group_name || "—" }}</p>
      <p><strong>Дата зачисления:</strong> {{ student.enrollment_date || "—" }}</p>
    </div>

    <h2>💬 Комментарии</h2>

    <div v-if="comments.length === 0" class="empty">Пока нет комментариев</div>

    <div v-for="c in comments" :key="c.id" class="comment">
      <div class="comment-header">
        <strong>{{ c.author_name }}</strong>
        <span class="date">{{ new Date(c.created_at).toLocaleString("ru-RU") }}</span>
      </div>
      <p>{{ c.text }}</p>
      <button class="btn-delete" @click="deleteComment(c.id)">Удалить</button>
    </div>

    <div class="add-comment">
      <h3>Добавить комментарий</h3>
      <input v-model="newAuthor" placeholder="Ваше имя" />
      <textarea v-model="newText" placeholder="Текст комментария" rows="3"></textarea>
      <button @click="addComment">Добавить</button>
    </div>
  </div>
</template>

<style scoped>
.detail {
  max-width: 700px;
}
.info-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.05);
  margin-bottom: 30px;
}
.info-card p {
  margin: 8px 0;
  font-size: 1.05em;
}
.comment {
  background: white;
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
  position: relative;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}
.date {
  color: #95a5a6;
  font-size: 0.85em;
}
.comment p {
  color: #555;
}
.btn-delete {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1em;
}
.add-comment {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.05);
  margin-top: 20px;
}
.add-comment h3 {
  margin-bottom: 15px;
}
.add-comment input, .add-comment textarea {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 0.95em;
}
.add-comment input:focus, .add-comment textarea:focus {
  border-color: #3498db;
  outline: none;
}
.add-comment button {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95em;
}
.add-comment button:hover {
  background: #2980b9;
}
.empty {
  color: #95a5a6;
  text-align: center;
  padding: 30px;
}
</style>