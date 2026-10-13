<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const payments = ref([])
const loans = ref([])

const paymentToAdd = ref({
  loan: '',
  payment_amount: ''
})

const paymentToEdit = ref({})

async function fetchData() {
  const [resPayments, resLoans] = await Promise.all([
    axios.get('/api/payments/'),
    axios.get('/api/loans/')
  ])
  payments.value = resPayments.data
  loans.value = resLoans.data
}

onBeforeMount(() => {
  fetchData()
})

async function onPaymentAdd() {
  await axios.post('/api/payments/', paymentToAdd.value)
  paymentToAdd.value = { loan: '', payment_amount: '' }
  await fetchData()
}

async function onPaymentDelete(item) {
  await axios.delete(`/api/payments/${item.id}/`)
  await fetchData()
}

function onPaymentEditClick(item) {
  paymentToEdit.value = { ...item }
}

async function onPaymentUpdate() {
  await axios.put(`/api/payments/${paymentToEdit.value.id}/`, paymentToEdit.value)
  await fetchData()
}
</script>

<template>
  <div>
    <h2>Платежи по займам</h2>

    <div class="card p-3 my-3 bg-light">
      <h5>Внести платёж:</h5>
      <form @submit.prevent.stop="onPaymentAdd" class="row g-2">
        <div class="col-md-6">
          <select class="form-select" v-model="paymentToAdd.loan" required>
            <option value="" disabled>Выберите заём</option>
            <option v-for="l in loans" :key="l.id" :value="l.id">Заём #{{ l.id }} (на сумму {{ l.amount }} руб.)</option>
          </select>
        </div>
        <div class="col-md-5">
          <input class="form-control" type="number" step="0.01" v-model="paymentToAdd.payment_amount" placeholder="Сумма платежа (руб.)" required>
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
          <th>ID займа</th>
          <th>Сумма платежа</th>
          <th>Дата и время</th>
          <th style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in payments" :key="item.id">
          <td>{{ item.id }}</td>
          <td>Заём #{{ item.loan }}</td>
          <td>{{ item.payment_amount }} руб.</td>
          <td>{{ item.payment_date }}</td>
          <td>
            <button 
              class="btn btn-success btn-sm me-2" 
              data-bs-toggle="modal" 
              data-bs-target="#editPaymentModal" 
              @click="onPaymentEditClick(item)"
            >
              Редактировать
            </button>
            <button class="btn btn-danger btn-sm" @click="onPaymentDelete(item)">Удалить</button>
          </td>
        </tr>
        <tr v-if="payments.length === 0">
          <td colspan="5" class="text-center text-muted">Платежей пока нет.</td>
        </tr>
      </tbody>
    </table>

    <div class="modal fade" id="editPaymentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактирование платежа</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Сумма платежа (руб.)</label>
              <input type="number" step="0.01" class="form-control" v-model="paymentToEdit.payment_amount">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onPaymentUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>