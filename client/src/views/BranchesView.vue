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
const branchPictureRef = ref()
const branchPictureUrl = ref()
const editBranchPictureRef = ref()
const activeModalImage = ref('')

function openImage(url) {
  activeModalImage.value = url
}

function onPictureChange() {
  if (branchPictureRef.value.files[0]) {
    branchPictureUrl.value = URL.createObjectURL(branchPictureRef.value.files[0])
  }
}

async function fetchBranches() {
  const response = await axios.get('/api/branches/')
  branches.value = response.data
}

onBeforeMount(() => {
  fetchBranches()
})

async function onBranchAdd() {
  const formData = new FormData()
  formData.append('name', branchToAdd.value.name)
  formData.append('city', branchToAdd.value.city)
  formData.append('address', branchToAdd.value.address)

  if (branchPictureRef.value && branchPictureRef.value.files[0]) {
    formData.append('picture', branchPictureRef.value.files[0])
  }

  await axios.post('/api/branches/', formData)
  
  branchToAdd.value = { name: '', city: '', address: '' }
  branchPictureUrl.value = null
  if (branchPictureRef.value) branchPictureRef.value.value = ''
  
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
  const formData = new FormData()
  formData.append('name', branchToEdit.value.name)
  formData.append('city', branchToEdit.value.city)
  formData.append('address', branchToEdit.value.address)

  if (editBranchPictureRef.value && editBranchPictureRef.value.files[0]) {
    formData.append('picture', editBranchPictureRef.value.files[0])
  }

  await axios.put(`/api/branches/${branchToEdit.value.id}/`, formData)
  await fetchBranches()
}
</script>

<template>
  <div>
    <h2>Филиалы компании</h2>

    <!-- Форма добавления филиала с выбором картинки -->
    <div class="card p-3 my-3 bg-light">
      <h5>Добавить новый филиал:</h5>
      <form @submit.prevent.stop="onBranchAdd" class="row g-2 align-items-center">
        <div class="col-md-3">
          <input class="form-control" type="text" v-model="branchToAdd.name" placeholder="Название филиала" required>
        </div>
        <div class="col-md-2">
          <input class="form-control" type="text" v-model="branchToAdd.city" placeholder="Город" required>
        </div>
        <div class="col-md-3">
          <input class="form-control" type="text" v-model="branchToAdd.address" placeholder="Адрес" required>
        </div>
        
        <div class="col-md-3">
          <input class="form-control" type="file" ref="branchPictureRef" @change="onPictureChange">
        </div>
        <div class="col-md-1">
          <button class="btn btn-primary w-100" type="submit">Добавить</button>
        </div>
        
        <div class="col-12 mt-2" v-if="branchPictureUrl">
          <span class="me-2 text-muted">Предпросмотр:</span>
          <img :src="branchPictureUrl" style="max-height: 50px; border-radius: 4px;" />
        </div>
      </form>
    </div>

    <!-- Таблица со списком филиалов -->
    <table class="table table-striped mt-3 align-middle">
      <thead>
        <tr>
          <th>ID</th>
          <th>Логотип / Фото</th>
          <th>Название</th>
          <th>Город</th>
          <th>Адрес</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in branches" :key="item.id">
          <td>{{ item.id }}</td>
          
          <td>
            <img 
              v-if="item.picture" 
              :src="item.picture" 
              style="max-height: 45px; cursor: pointer; border-radius: 4px;" 
              data-bs-toggle="modal" 
              data-bs-target="#imageModal" 
              @click="openImage(item.picture)" 
              title="Нажмите, чтобы увеличить"
            />
            <span v-else class="text-muted">Нет фото</span>
          </td>
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
          <td colspan="6" class="text-center text-muted">Записей пока нет.</td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно редактирования (с возможностью заменить картинку) -->
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
            <div class="mb-3">
              <label class="form-label">Заменить картинку</label>
              <input class="form-control" type="file" ref="editBranchPictureRef">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onBranchUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для просмотра увеличенной картинки по клику -->
    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр изображения</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="activeModalImage" style="max-width: 100%; max-height: 500px; border-radius: 6px;" />
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
</style>