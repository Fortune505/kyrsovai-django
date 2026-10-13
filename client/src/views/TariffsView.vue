<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const tariffs = ref([])

const tariffToAdd = ref({
  name: '',
  interest_rate: '',
  max_amount: '',
  term_days: ''
})

const tariffToEdit = ref({})

async function fetchTariffs() {
  const response = await axios.get('/api/tariffs/')
  tariffs.value = response.data
}

onBeforeMount(() => {
  fetchTariffs()
})

async function onTariffAdd() {
  await axios.post('/api/tariffs/', tariffToAdd.value)
  tariffToAdd.value = { name: '', interest_rate: '', max_amount: '', term_days: '' }
  await fetchTariffs()
}

async function onTariffDelete(item) {
  await axios.delete(`/api/tariffs/${item.id}/`)
  await fetchTariffs()
}

function onTariffEditClick(item) {
  tariffToEdit.value = { ...item }
}

async function onTariffUpdate() {
  await axios.put(`/api/tariffs/${tariffToEdit.value.id}/`, tariffToEdit.value)
  await fetchTariffs()
}
</script>

<template>
  <div>
    <h2>Кредитные тарифы</h2>

    <div class="card p-3 my-3 bg-light">
      <h5>Добавить новый тариф:</h5>
      <form @submit.prevent.stop="onTariffAdd" class="row g-2">
        <div class="col-md-3">
          <input class="form-control" type="text" v-model="tariffToAdd.name" placeholder="Название тарифа" required>
        </div>
        <div class="col-md-3">
          <input class="form-control" type="number" step="0.01" v-model="tariffToAdd.interest_rate" placeholder="Ставка (% в день)" required>
        </div>
        <div class="col-md-3">
          <input class="form-control" type="number" step="0.01" v-model="tariffToAdd.max_amount" placeholder="Макс. сумма (руб.)" required>
        </div>
        <div class="col-md-2">
          <input class="form-control" type="number" v-model="tariffToAdd.term_days" placeholder="Срок (дней)" required>
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
          <th>Название</th>
          <th>Ставка (%/день)</th>
          <th>Макс. сумма</th>
          <th>Срок (дней)</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in tariffs" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.interest_rate }}%</td>
          <td>{{ item.max_amount }} руб.</td>
          <td>{{ item.term_days }}</td>
          <td>
            <button 
              class="btn btn-success btn-sm me-2" 
              data-bs-toggle="modal" 
              data-bs-target="#editTariffModal" 
              @click="onTariffEditClick(item)"
            >
              Редактировать
            </button>
            <button class="btn btn-danger btn-sm" @click="onTariffDelete(item)">Удалить</button>
          </td>
        </tr>
        <tr v-if="tariffs.length === 0">
          <td colspan="6" class="text-center text-muted">Тарифов пока нет.</td>
        </tr>
      </tbody>
    </table>

    <div class="modal fade" id="editTariffModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактирование тарифа</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название тарифа</label>
              <input type="text" class="form-control" v-model="tariffToEdit.name">
            </div>
            <div class="mb-3">
              <label class="form-label">Ставка (% в день)</label>
              <input type="number" step="0.01" class="form-control" v-model="tariffToEdit.interest_rate">
            </div>
            <div class="mb-3">
              <label class="form-label">Максимальная сумма (руб.)</label>
              <input type="number" step="0.01" class="form-control" v-model="tariffToEdit.max_amount">
            </div>
            <div class="mb-3">
              <label class="form-label">Срок (дней)</label>
              <input type="number" class="form-control" v-model="tariffToEdit.term_days">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onTariffUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>