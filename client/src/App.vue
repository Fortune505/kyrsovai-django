<script setup>
import { ref, onBeforeMount } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import axios from 'axios'
import Cookies from 'js-cookie'

const currentUser = ref({
  is_authenticated: false,
  is_staff: false,
  is_superuser: false,
  username: ''
})

const authForm = ref({ username: '', password: '', email: '' })
const authError = ref('')

// Проверка сессии
async function checkAuth() {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  try {
    const res = await axios.get('/api/users/current/')
    currentUser.value = res.data
  } catch (e) {
    currentUser.value = { is_authenticated: false, is_staff: false, is_superuser: false }
  }
}

onBeforeMount(() => {
  checkAuth()
})

// Вход в систему
async function onLogin() {
  authError.value = ''
  try {
    await axios.post('/api/users/login_user/', {
      username: authForm.value.username,
      password: authForm.value.password
    })
    authForm.value = { username: '', password: '', email: '' }
    await checkAuth()
    window.location.reload()
  } catch (err) {
    authError.value = err.response?.data?.error || 'Ошибка входа'
  }
}

// Регистрация
async function onRegister() {
  authError.value = ''
  try {
    await axios.post('/api/users/register_user/', authForm.value)
    authForm.value = { username: '', password: '', email: '' }
    await checkAuth()
    window.location.reload()
  } catch (err) {
    authError.value = err.response?.data?.error || 'Ошибка регистрации'
  }
}

// Выход из системы
async function onLogout() {
  await axios.post('/api/users/logout_user/')
  currentUser.value = { is_authenticated: false, is_staff: false, is_superuser: false }
  window.location.href = '/'
}
</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4 shadow">
      <div class="container">
        <RouterLink class="navbar-brand fw-bold text-info" to="/">Синий Крест Давида</RouterLink>

        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <!-- Главная и Филиалы видны абсолютно всем -->
            <li class="nav-item"><RouterLink class="nav-link" to="/">Главная</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/branches">Филиалы</RouterLink></li>
            
            <!-- Тарифы: видны ТОЛЬКО персоналу (Менеджерам и Админам) для настройки условий -->
            <li v-if="currentUser.is_staff || currentUser.is_superuser" class="nav-item">
              <RouterLink class="nav-link" to="/tariffs">Тарифы</RouterLink>
            </li>
            
            <!-- Займы и Платежи: видны только авторизованным (Клиентам, Менеджерам, Админам) -->
            <li v-if="currentUser.is_authenticated" class="nav-item">
              <RouterLink class="nav-link" to="/loans">Займы</RouterLink>
            </li>
            <li v-if="currentUser.is_authenticated" class="nav-item">
              <RouterLink class="nav-link" to="/payments">Платежи</RouterLink>
            </li>

            <!-- Пользователи: видны только администратору -->
            <li v-if="currentUser.is_superuser" class="nav-item">
              <RouterLink class="nav-link text-warning" to="/users">Пользователи</RouterLink>
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle text-light" href="#" role="button" data-bs-toggle="dropdown">
                {{ currentUser.username || 'Гость' }}
                <span v-if="currentUser.is_superuser" class="badge bg-danger ms-1">Админ</span>
                <span v-else-if="currentUser.is_staff" class="badge bg-warning text-dark ms-1">Менеджер</span>
                <span v-else-if="currentUser.is_authenticated" class="badge bg-success ms-1">Клиент</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <!-- Меню для авторизованного пользователя -->
                <template v-if="currentUser.is_authenticated">
                  <li><a class="dropdown-item" href="/admin">Панель управления (Django)</a></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item text-danger" href="#" @click.prevent="onLogout">Выйти из аккаунта</a></li>
                </template>

                <!-- Меню для гостя -->
                <template v-else>
                  <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#loginModal">Войти</a></li>
                  <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#registerModal">Создать аккаунт</a></li>
                </template>
              </ul>
            </li>
          </ul>

        </div>
      </div>
    </nav>

    <div class="container">
      <RouterView />
    </div>
    <!-- Модальное окно входа -->
    <div class="modal fade" id="loginModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Вход в систему</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="onLogin">
            <div class="modal-body">
              <div v-if="authError" class="alert alert-danger p-2">{{ authError }}</div>
              <div class="mb-3">
                <label class="form-label">Логин</label>
                <input class="form-control" type="text" v-model="authForm.username" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Пароль</label>
                <input class="form-control" type="password" v-model="authForm.password" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
              <button type="submit" class="btn btn-primary">Войти</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal fade" id="registerModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">Создание аккаунта</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="onRegister">
            <div class="modal-body">
              <div v-if="authError" class="alert alert-danger p-2">{{ authError }}</div>
              <div class="mb-3">
                <label class="form-label">Логин</label>
                <input class="form-control" type="text" v-model="authForm.username" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Email (необязательно)</label>
                <input class="form-control" type="email" v-model="authForm.email">
              </div>
              <div class="mb-3">
                <label class="form-label">Пароль</label>
                <input class="form-control" type="password" v-model="authForm.password" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
              <button type="submit" class="btn btn-success">Зарегистрироваться</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.nav-link.router-link-active {
  color: #0dcaf0 !important;
  font-weight: bold;
}
</style>