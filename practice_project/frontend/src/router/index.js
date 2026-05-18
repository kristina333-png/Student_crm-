import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import StudentsPage from "../pages/StudentsPage.vue";
import CreateStudentPage from "../pages/CreateStudentPage.vue";
import EditStudentPage from "../pages/EditStudentPage.vue";
import AboutPage from "../pages/AboutPage.vue";
import StudentDetailPage from "../pages/StudentDetailPage.vue";
import GroupsPage from "../pages/GroupsPage.vue";
import CreateGroupPage from "../pages/CreateGroupPage.vue";
import EditGroupPage from "../pages/EditGroupPage.vue";
import GradesPage from "../pages/GradesPage.vue";
import CreateGradePage from "../pages/CreateGradePage.vue";
import EditGradePage from "../pages/EditGradePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/students", component: StudentsPage },
  { path: "/students/create", component: CreateStudentPage },
  { path: "/students/:id/edit", component: EditStudentPage },
  { path: "/about", component: AboutPage },
  { path: "/students/:id", component: StudentDetailPage },
  { path: "/groups", component: GroupsPage },
  { path: "/groups/create", component: CreateGroupPage },
  { path: "/groups/:id/edit", component: EditGroupPage },
  { path: "/grades", component: GradesPage },
  { path: "/grades/create", component: CreateGradePage },
  { path: "/grades/:id/edit", component: EditGradePage },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const publicPages = ["/", "/about"];
  const token = localStorage.getItem("accessToken");
  const role = localStorage.getItem("userRole");

  if (to.path === "/login" && token) {
    next("/students");
    return;
  }

  if (!token && !publicPages.includes(to.path) && to.path !== "/login") {
    next("/login");
  } else {
    next();
  }
});

export default router;