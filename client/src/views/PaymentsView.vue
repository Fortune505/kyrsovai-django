<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const payments = ref([])
const loans = ref([])
const currentUser = ref({ is_authenticated: false, is_staff: false, is_superuser: false })

const paymentToAdd = ref({ loan: '', payment_amount: '' })
const paymentToEdit = ref({})

async function fetchData() {
  const [resPayments, resLoans] = await Promise.all([
    axios.get('/api/payments/'),
    axios.get('/api/loans/')
  ])
  payments.value = resPayments.data
  loans.value = resLoans.data
}

onBeforeMount(async () => {
  try {
    const uRes = await axios.get('/api/users/current/')
    currentUser.value = uRes.data
  } catch (e) {}
  await fetchData()
})

async function onPaymentAdd() {
  await axios.post('/api/payments/', paymentToAdd.value)
  paymentToAdd.value = { loan: '', payment_amount: '' }
  await fetchData()
}

async function onPaymentDelete(item) {
  if (!confirm('Удалить эту запись о платеже?')) return
  await axios.delete(`/api/payments/${item.id}/`)
  await fetchData()
}

function onPaymentEditClick(item) {
  paymentToEdit.value = { ...item }
}

async function onPaymentUpdate() {
  await axios.patch(`/api/payments/${paymentToEdit.value.id}/`, paymentToEdit.value)
  await fetchData()
}
</script>

<template>
  <div>
    <h2>Платежи по займам</h2>

    <!-- Внесение платежа: для клиентов или персонала -->
    <div class="card p-3 my-3 bg-light shadow-sm">
      <h5>Внести платёж по займу:</h5>
      <form @submit.prevent.stop="onPaymentAdd" class="row g-2 align-items-center">
        <div class="col-md-6">
          <select class="form-select" v-model="paymentToAdd.loan" required>
            <option value="" disabled>Выберите договор займа</option>
            <option v-for="l in loans" :key="l.id" :value="l.id">
              Заём #{{ l.id }} ({{ l.amount }} руб.) — {{ l.client_name }}
            </option>
          </select>
        </div>
        <div class="col-md-5">
          <input class="form-control" type="number" step="0.01" v-model="paymentToAdd.payment_amount" placeholder="Сумма платежа (руб.)" required>
        </div>
        <div class="col-md-1">
          <button class="btn btn-primary w-100" type="submit">Оплатить</button>
        </div>
      </form>
    </div>

    <!-- Таблица платежей -->
    <table class="table table-striped mt-3 align-middle">
      <thead>
        <tr>
          <th>ID</th>
          <th>Номер займа</th>
          <th>Сумма платежа</th>
          <th>Дата и время</th>
          <th v-if="currentUser.is_staff || currentUser.is_superuser" style="width: 220px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in payments" :key="item.id">
          <td>{{ item.id }}</td>
          <td class="fw-bold">Заём #{{ item.loan }}</td>
          <td class="text-success fw-bold">{{ item.payment_amount }} руб.</td>
          <td>{{ item.payment_date }}</td>
          <td v-if="currentUser.is_staff || currentUser.is_superuser">
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
          <td :colspan="currentUser.is_staff || currentUser.is_superuser ? 5 : 4" class="text-center text-muted">
            Платежей пока нет.
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно редактирования платежа -->
    <div class="modal fade" id="editPaymentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Редактирование платежа</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
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

<style scoped>
</style>