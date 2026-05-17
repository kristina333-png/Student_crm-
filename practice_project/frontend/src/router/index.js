import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import StudentsPage from "../pages/StudentsPage.vue";
import AboutPage from "../pages/AboutPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/students", component: StudentsPage },
  { path: "/about", component: AboutPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;