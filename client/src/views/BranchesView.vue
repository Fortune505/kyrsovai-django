<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const branches = ref([])

const branchToAdd = ref({
  name: '',
  city: '',
  address: ''
})

const branchToEdit = ref({})

async function fetchBranches() {
  const response = await axios.get('/api/branches/')
  branches.value = response.data
}

onBeforeMount(() => {
  fetchBranches()
})

async function onBranchAdd() {
  await axios.post('/api/branches/', branchToAdd.value)
  branchToAdd.value = { name: '', city: '', address: '' }
  await fetchBranches()
}

async function onBranchDelete(item) {
  await axios.delete(`/api/branches/${item.id}/`)
  await fetchBranches()
}

function onBranchEditClick(item) {
  branchToEdit.value = { ...item }
}

async function onBranchUpdate() {
  await axios.put(`/api/branches/${branchToEdit.value.id}/`, branchToEdit.value)
  await fetchBranches()
}
</script>

<template>
  <div>
    <h2>Филиалы компании</h2>

    <div class="card p-3 my-3 bg-light">
      <h5>Добавить новый филиал:</h5>
      <form @submit.prevent.stop="onBranchAdd" class="row g-2">
        <div class="col-md-4">
          <input class="form-control" type="text" v-model="branchToAdd.name" placeholder="Название филиала" required>
        </div>
        <div class="col-md-3">
          <input class="form-control" type="text" v-model="branchToAdd.city" placeholder="Город" required>
        </div>
        <div class="col-md-4">
          <input class="form-control" type="text" v-model="branchToAdd.address" placeholder="Адрес" required>
        </div>
        <div class="col-md-1">
          <button class="btn btn-primary w-100" type="submit">Добавить</button>
        </div>
      </form>
    </div>

    <table class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Город</th>
          <th>Адрес</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in branches" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.city }}</td>
          <td>{{ item.address }}</td>
          <td>
            <button 
              class="btn btn-success btn-sm me-2" 
              data-bs-toggle="modal" 
              data-bs-target="#editBranchModal" 
              @click="onBranchEditClick(item)"
            >
              Редактировать
            </button>
            <button class="btn btn-danger btn-sm" @click="onBranchDelete(item)">Удалить</button>
          </td>
        </tr>
        <tr v-if="branches.length === 0">
          <td colspan="5" class="text-center text-muted">Записей пока нет.</td>
        </tr>
      </tbody>
    </table>

    <div class="modal fade" id="editBranchModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактирование филиала</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название филиала</label>
              <input type="text" class="form-control" v-model="branchToEdit.name">
            </div>
            <div class="mb-3">
              <label class="form-label">Город</label>
              <input type="text" class="form-control" v-model="branchToEdit.city">
            </div>
            <div class="mb-3">
              <label class="form-label">Адрес</label>
              <input type="text" class="form-control" v-model="branchToEdit.address">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onBranchUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>