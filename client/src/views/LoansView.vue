<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const loans = ref([])
const users = ref([])
const tariffs = ref([])
const branches = ref([])

const currentUser = ref({
  is_authenticated: false,
  is_staff: false,
  is_superuser: false,
  username: ''
})

const selectedUserFilter = ref('')

const loanToAdd = ref({
  tariff: '',
  branch: '',
  amount: '',
  status: 'active'
})

const loanToEdit = ref({})
const loanPictureRef = ref()
const loanPictureUrl = ref()
const editLoanPictureRef = ref()
const activeModalImage = ref('')

function openImage(url) {
  activeModalImage.value = url
}

function onPictureChange() {
  if (loanPictureRef.value && loanPictureRef.value.files[0]) {
    loanPictureUrl.value = URL.createObjectURL(loanPictureRef.value.files[0])
  }
}

// Загрузка данных
async function fetchData() {
  let loansUrl = '/api/loans/'
  if (selectedUserFilter.value) {
    loansUrl += `?user=${selectedUserFilter.value}`
  }

  const [resLoans, resUsers, resTariffs, resBranches] = await Promise.all([
    axios.get(loansUrl),
    axios.get('/api/users/'),
    axios.get('/api/tariffs/'),
    axios.get('/api/branches/')
  ])
  loans.value = resLoans.data
  users.value = resUsers.data
  tariffs.value = resTariffs.data
  branches.value = resBranches.data
}

onBeforeMount(async () => {
  try {
    const userRes = await axios.get('/api/users/current/')
    currentUser.value = userRes.data
  } catch (e) {
    currentUser.value = { is_authenticated: false, is_staff: false, is_superuser: false }
  }
  await fetchData()
})

// Оформление займа
async function onLoanAdd() {
  const formData = new FormData()
  formData.append('tariff', loanToAdd.value.tariff)
  if (loanToAdd.value.branch) {
    formData.append('branch', loanToAdd.value.branch)
  }
  formData.append('amount', loanToAdd.value.amount)
  formData.append('status', loanToAdd.value.status)

  if (loanPictureRef.value && loanPictureRef.value.files[0]) {
    formData.append('picture', loanPictureRef.value.files[0])
  }

  await axios.post('/api/loans/', formData)

  loanToAdd.value = { tariff: '', branch: '', amount: '', status: 'active' }
  loanPictureUrl.value = null
  if (loanPictureRef.value) loanPictureRef.value.value = ''

  await fetchData()
}

// Удаление займа
async function onLoanDelete(item) {
  if (!confirm('Удалить этот договор займа?')) return
  await axios.delete(`/api/loans/${item.id}/`)
  await fetchData()
}

// Подготовка к редактированию
function onLoanEditClick(item) {
  loanToEdit.value = { ...item }
}

// Сохранение изменений займа
async function onLoanUpdate() {
  const formData = new FormData()
  formData.append('tariff', loanToEdit.value.tariff)
  if (loanToEdit.value.branch) {
    formData.append('branch', loanToEdit.value.branch)
  }
  formData.append('amount', loanToEdit.value.amount)
  formData.append('status', loanToEdit.value.status)

  if (editLoanPictureRef.value && editLoanPictureRef.value.files[0]) {
    formData.append('picture', editLoanPictureRef.value.files[0])
  }

  await axios.patch(`/api/loans/${loanToEdit.value.id}/`, formData)
  await fetchData()
}
</script>

<template>
  <div>
    <h2>Договоры займа</h2>

    <!-- Фильтр по пользователям: виден только персоналу (администраторам и менеджерам) -->
    <div v-if="currentUser.is_staff || currentUser.is_superuser" class="row my-3 align-items-center bg-white p-3 border rounded shadow-sm">
      <div class="col-auto fw-bold text-secondary">Фильтр по пользователю (для персонала):</div>
      <div class="col-md-4">
        <select class="form-select form-select-sm" v-model="selectedUserFilter" @change="fetchData">
          <option value="">Все пользователи (без фильтра)</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
        </select>
      </div>
    </div>

    <!-- Форма ручного добавления: видна только персоналу -->
    <div v-if="currentUser.is_staff || currentUser.is_superuser" class="card p-3 my-3 bg-light shadow-sm">
      <h5 class="text-primary">Оформить новый заём:</h5>
      <form @submit.prevent.stop="onLoanAdd" class="row g-2 align-items-center">
        <div class="col-md-3">
          <select class="form-select" v-model="loanToAdd.tariff" required>
            <option value="" disabled>Выберите тариф</option>
            <option v-for="t in tariffs" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="loanToAdd.branch">
            <option value="">Без филиала</option>
            <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <input class="form-control" type="number" step="0.01" v-model="loanToAdd.amount" placeholder="Сумма" required>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="loanToAdd.status">
            <option value="active">Активен</option>
            <option value="paid">Погашен</option>
            <option value="overdue">Просрочен</option>
          </select>
        </div>
        <div class="col-md-2">
          <input class="form-control" type="file" ref="loanPictureRef" @change="onPictureChange">
        </div>
        <div class="col-md-1">
          <button class="btn btn-primary w-100" type="submit">+</button>
        </div>

        <div class="col-12 mt-2" v-if="loanPictureUrl">
          <span class="me-2 text-muted">Предпросмотр:</span>
          <img :src="loanPictureUrl" style="max-height: 50px; border-radius: 4px;" />
        </div>
      </form>
    </div>

    <!-- Таблица договоров займа -->
    <table class="table table-striped mt-3 align-middle">
      <thead>
        <tr>
          <th>ID</th>
          <th>Эмблема / Договор</th>
          <th>Клиент</th>
          <th>Тариф</th>
          <th>Филиал</th>
          <th>Сумма</th>
          <th>Дата выдачи</th>
          <th>Статус</th>
          <!-- Колонка «Действия» видна только персоналу -->
          <th v-if="currentUser.is_staff || currentUser.is_superuser" style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in loans" :key="item.id">
          <td>{{ item.id }}</td>
          <td>
            <img 
              :src="item.picture || '/default_loan.png'" 
              style="max-height: 45px; cursor: pointer; border-radius: 4px;" 
              data-bs-toggle="modal" 
              data-bs-target="#loanImageModal" 
              @click="openImage(item.picture || '/default_loan.png')" 
              title="Нажмите, чтобы рассмотреть ближе"
            />
          </td>
          <td class="fw-bold">{{ item.client_name }}</td>
          <td>{{ item.tariff_name }}</td>
          <td>{{ item.branch_name || '—' }}</td>
          <td>{{ item.amount }} руб.</td>
          <td>{{ item.issue_date }}</td>
          <td>
            <span :class="{
              'badge bg-primary': item.status === 'active',
              'badge bg-success': item.status === 'paid',
              'badge bg-danger': item.status === 'overdue'
            }">{{ item.status }}</span>
          </td>
          <!-- Кнопки управления доступны только менеджерам и админам -->
          <td v-if="currentUser.is_staff || currentUser.is_superuser">
            <button 
              class="btn btn-success btn-sm me-2" 
              data-bs-toggle="modal" 
              data-bs-target="#editLoanModal" 
              @click="onLoanEditClick(item)"
            >
              Редактировать
            </button>
            <button class="btn btn-danger btn-sm" @click="onLoanDelete(item)">Удалить</button>
          </td>
        </tr>
        <tr v-if="loans.length === 0">
          <td :colspan="currentUser.is_staff || currentUser.is_superuser ? 9 : 8" class="text-center text-muted">
            Займов пока нет.
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно редактирования займа -->
    <div class="modal fade" id="editLoanModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Редактирование займа</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Сумма займа (руб.)</label>
              <input type="number" step="0.01" class="form-control" v-model="loanToEdit.amount">
            </div>
            <div class="mb-3">
              <label class="form-label">Статус</label>
              <select class="form-select" v-model="loanToEdit.status">
                <option value="active">Активен</option>
                <option value="paid">Погашен</option>
                <option value="overdue">Просрочен</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Заменить скан документа</label>
              <input class="form-control" type="file" ref="editLoanPictureRef">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onLoanUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно просмотра увеличенного документа -->
    <div class="modal fade" id="loanImageModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр документа займа</h5>
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