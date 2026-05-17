import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import StudentsPage from "../pages/StudentsPage.vue";
import CreateStudentPage from "../pages/CreateStudentPage.vue";
import EditStudentPage from "../pages/EditStudentPage.vue";
import AboutPage from "../pages/AboutPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/students", component: StudentsPage },
  { path: "/students/create", component: CreateStudentPage },
  { path: "/students/:id/edit", component: EditStudentPage },
  { path: "/about", component: AboutPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;