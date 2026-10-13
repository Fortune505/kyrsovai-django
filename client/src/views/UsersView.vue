<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const users = ref([])

const userToAdd = ref({
  username: '',
  email: ''
})

const userToEdit = ref({})

async function fetchUsers() {
  const response = await axios.get('/api/users/')
  users.value = response.data
}

onBeforeMount(() => {
  fetchUsers()
})

async function onUserAdd() {
  await axios.post('/api/users/', userToAdd.value)
  userToAdd.value = { username: '', email: '' }
  await fetchUsers()
}

async function onUserDelete(item) {
  await axios.delete(`/api/users/${item.id}/`)
  await fetchUsers()
}

function onUserEditClick(item) {
  userToEdit.value = { ...item }
}

async function onUserUpdate() {
  await axios.put(`/api/users/${userToEdit.value.id}/`, userToEdit.value)
  await fetchUsers()
}
</script>

<template>
  <div>
    <h2>Клиенты и пользователи</h2>

    <div class="card p-3 my-3 bg-light">
      <h5>Добавить пользователя:</h5>
      <form @submit.prevent.stop="onUserAdd" class="row g-2">
        <div class="col-md-6">
          <input class="form-control" type="text" v-model="userToAdd.username" placeholder="Логин / Имя пользователя" required>
        </div>
        <div class="col-md-5">
          <input class="form-control" type="email" v-model="userToAdd.email" placeholder="Электронная почта">
        </div>
        <div class="col-md-1">
          <button class="btn btn-primary w-100" type="submit">+</button>
        </div>
      </form>
    </div>

    <table class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>Логин</th>
          <th>Email</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in users" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.email || '—' }}</td>
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

    <div class="modal fade" id="editUserModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактирование пользователя</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
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