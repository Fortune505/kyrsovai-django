<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const loans = ref([])
const users = ref([])
const tariffs = ref([])
const branches = ref([])

const loanToAdd = ref({
  client: '',
  tariff: '',
  branch: '',
  amount: '',
  status: 'active'
})

const loanToEdit = ref({})

async function fetchData() {
  const [resLoans, resUsers, resTariffs, resBranches] = await Promise.all([
    axios.get('/api/loans/'),
    axios.get('/api/users/'),
    axios.get('/api/tariffs/'),
    axios.get('/api/branches/')
  ])
  loans.value = resLoans.data
  users.value = resUsers.data
  tariffs.value = resTariffs.data
  branches.value = resBranches.data
}

onBeforeMount(() => {
  fetchData()
})

async function onLoanAdd() {
  await axios.post('/api/loans/', loanToAdd.value)
  loanToAdd.value = { client: '', tariff: '', branch: '', amount: '', status: 'active' }
  await fetchData()
}

async function onLoanDelete(item) {
  await axios.delete(`/api/loans/${item.id}/`)
  await fetchData()
}

function onLoanEditClick(item) {
  loanToEdit.value = { ...item }
}

async function onLoanUpdate() {
  await axios.put(`/api/loans/${loanToEdit.value.id}/`, loanToEdit.value)
  await fetchData()
}
</script>

<template>
  <div>
    <h2>Договоры займа</h2>

    <div class="card p-3 my-3 bg-light">
      <h5>Оформить новый заём:</h5>
      <form @submit.prevent.stop="onLoanAdd" class="row g-2">
        <div class="col-md-3">
          <select class="form-select" v-model="loanToAdd.client" required>
            <option value="" disabled>Выберите клиента</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="loanToAdd.tariff" required>
            <option value="" disabled>Тариф</option>
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
          <input class="form-control" type="number" step="0.01" v-model="loanToAdd.amount" placeholder="Сумма (руб.)" required>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="loanToAdd.status">
            <option value="active">Активен</option>
            <option value="paid">Погашен</option>
            <option value="overdue">Просрочен</option>
          </select>
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
          <th>Клиент (ID)</th>
          <th>Тариф (ID)</th>
          <th>Филиал (ID)</th>
          <th>Сумма</th>
          <th>Дата выдачи</th>
          <th>Статус</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in loans" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.client }}</td>
          <td>{{ item.tariff }}</td>
          <td>{{ item.branch || '—' }}</td>
          <td>{{ item.amount }} руб.</td>
          <td>{{ item.issue_date }}</td>
          <td>
            <span :class="{
              'badge bg-primary': item.status === 'active',
              'badge bg-success': item.status === 'paid',
              'badge bg-danger': item.status === 'overdue'
            }">{{ item.status }}</span>
          </td>
          <td>
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
          <td colspan="8" class="text-center text-muted">Займов пока нет.</td>
        </tr>
      </tbody>
    </table>

    <div class="modal fade" id="editLoanModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактирование займа</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Сумма займа</label>
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
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onLoanUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>