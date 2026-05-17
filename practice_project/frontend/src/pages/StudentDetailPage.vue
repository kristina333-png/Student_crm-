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
  <div v-if="student">
    <h1>{{ student.first_name }} {{ student.last_name }}</h1>
    <p>Email: {{ student.email }}</p>
    <p>Телефон: {{ student.phone || "—" }}</p>
    <p>Группа: {{ student.group_name || "—" }}</p>

    <h2>Комментарии</h2>
    <div v-for="c in comments" :key="c.id" class="comment">
      <strong>{{ c.author_name }}</strong> ({{ new Date(c.created_at).toLocaleString() }})
      <p>{{ c.text }}</p>
      <button @click="deleteComment(c.id)">Удалить</button>
    </div>

    <div class="add-comment">
      <input v-model="newAuthor" placeholder="Ваше имя" />
      <textarea v-model="newText" placeholder="Комментарий"></textarea>
      <button @click="addComment">Добавить</button>
    </div>
  </div>
</template>

<style scoped>
.comment {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
}
.add-comment {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 15px;
  max-width: 400px;
}
.add-comment input, .add-comment textarea {
  padding: 6px;
}
</style>