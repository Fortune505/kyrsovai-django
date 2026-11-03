<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const users = ref([])

const userToAdd = ref({
  username: '',
  email: '',
  password: '',
  roleType: 'client'
})

const userToEdit = ref({
  id: null,
  username: '',
  email: '',
  roleType: 'client'
})

async function fetchUsers() {
  const response = await axios.get('/api/users/')
  users.value = response.data
}

onBeforeMount(() => {
  fetchUsers()
})

async function onUserAdd() {
  const payload = {
    username: userToAdd.value.username,
    email: userToAdd.value.email,
    password: userToAdd.value.password || 'password123',
    is_staff: userToAdd.value.roleType === 'manager' || userToAdd.value.roleType === 'admin',
    is_superuser: userToAdd.value.roleType === 'admin'
  }

  await axios.post('/api/users/', payload)
  userToAdd.value = { username: '', email: '', password: '', roleType: 'client' }
  await fetchUsers()
}

async function onUserDelete(item) {
  if (!confirm(`Удалить пользователя ${item.username}?`)) return
  await axios.delete(`/api/users/${item.id}/`)
  await fetchUsers()
}

// Запоминаем текущую роль при открытии редактирования
function onUserEditClick(item) {
  let role = 'client'
  if (item.is_superuser) role = 'admin'
  else if (item.is_staff) role = 'manager'

  userToEdit.value = { 
    id: item.id,
    username: item.username,
    email: item.email,
    roleType: role 
  }
}

// Сохраняем измененную роль и данные
async function onUserUpdate() {
  const payload = {
    username: userToEdit.value.username,
    email: userToEdit.value.email,
    is_staff: userToEdit.value.roleType === 'manager' || userToEdit.value.roleType === 'admin',
    is_superuser: userToEdit.value.roleType === 'admin'
  }

  await axios.patch(`/api/users/${userToEdit.value.id}/`, payload)
  await fetchUsers()
}
</script>

<template>
  <div>
    <h2>Управление пользователями и роли</h2>

    <!-- Форма создания -->
    <div class="card p-3 my-3 bg-light shadow-sm">
      <h5>Добавить нового пользователя:</h5>
      <form @submit.prevent.stop="onUserAdd" class="row g-2 align-items-center">
        <div class="col-md-3">
          <input class="form-control" type="text" v-model="userToAdd.username" placeholder="Логин" required>
        </div>
        <div class="col-md-3">
          <input class="form-control" type="email" v-model="userToAdd.email" placeholder="Email">
        </div>
        <div class="col-md-2">
          <input class="form-control" type="password" v-model="userToAdd.password" placeholder="Пароль" required>
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="userToAdd.roleType">
            <option value="client">Роль: Клиент</option>
            <option value="manager">Роль: Менеджер</option>
            <option value="admin">Роль: Администратор</option>
          </select>
        </div>
        <div class="col-md-1">
          <button class="btn btn-primary w-100" type="submit">+</button>
        </div>
      </form>
    </div>

    <!-- Таблица пользователей с ролями -->
    <table class="table table-striped mt-3 align-middle">
      <thead>
        <tr>
          <th>ID</th>
          <th>Логин</th>
          <th>Email</th>
          <th>Роль</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in users" :key="item.id">
          <td>{{ item.id }}</td>
          <td class="fw-bold">{{ item.username }}</td>
          <td>{{ item.email || '—' }}</td>
          <td>
            <span :class="{
              'badge bg-danger': item.is_superuser,
              'badge bg-warning text-dark': item.is_staff && !item.is_superuser,
              'badge bg-success': !item.is_staff && !item.is_superuser
            }">
              {{ item.role }}
            </span>
          </td>
          <td>
            <button 
              class="btn btn-success btn-sm me-2" 
              data-bs-toggle="modal" 
              data-bs-target="#editUserModal" 
              @click="onUserEditClick(item)"
            >
              Редактировать
            </button>
            <button class="btn btn-danger btn-sm" @click="onUserDelete(item)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно редактирования со сменой роли -->
    <div class="modal fade" id="editUserModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Редактирование пользователя</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Логин</label>
              <input type="text" class="form-control" v-model="userToEdit.username">
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" class="form-control" v-model="userToEdit.email">
            </div>
            <!-- Выбор роли при редактировании -->
            <div class="mb-3">
              <label class="form-label fw-bold">Роль пользователя</label>
              <select class="form-select" v-model="userToEdit.roleType">
                <option value="client">Клиент (только личный кабинет)</option>
                <option value="manager">Менеджер (управление займами и филиалами)</option>
                <option value="admin">Администратор (полный доступ)</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUserUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>