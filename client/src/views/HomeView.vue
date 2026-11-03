<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const tariffs = ref([])
const branches = ref([])
const currentUser = ref({ is_authenticated: false })

const selectedTariff = ref(null)
const loanForm = ref({ amount: '', branch: '' })
const loanPictureRef = ref()

async function fetchData() {
  const [resTariffs, resBranches] = await Promise.all([
    axios.get('/api/tariffs/'),
    axios.get('/api/branches/')
  ])
  tariffs.value = resTariffs.data
  branches.value = resBranches.data
}

onBeforeMount(async () => {
  try {
    const uRes = await axios.get('/api/users/current/')
    currentUser.value = uRes.data
  } catch (e) {}
  await fetchData()
})

function openApplyModal(tariff) {
  selectedTariff.value = tariff
  loanForm.value.amount = tariff.max_amount
  loanForm.value.branch = ''
}

async function submitLoan() {
  const formData = new FormData()
  formData.append('tariff', selectedTariff.value.id)
  if (loanForm.value.branch) {
    formData.append('branch', loanForm.value.branch)
  }
  formData.append('amount', loanForm.value.amount)
  formData.append('status', 'active')

  if (loanPictureRef.value && loanPictureRef.value.files[0]) {
    formData.append('picture', loanPictureRef.value.files[0])
  }

  await axios.post('/api/loans/', formData)
  router.push('/loans')
}
</script>

<template>
  <div>
    <div class="p-4 mb-4 bg-light rounded-3 border text-center shadow-sm">
      <h1 class="display-6 fw-bold text-primary">Микрозайм «Синий Крест Давида»</h1>
      <p class="lead text-muted">Быстрые финансовые решения на прозрачных условиях. Выберите подходящий тариф ниже:</p>
    </div>

    <h3 class="mb-3">Доступные тарифы займов:</h3>
    <div class="row g-4">
      <div class="col-md-4 col-sm-6" v-for="tariff in tariffs" :key="tariff.id">
        <div class="card h-100 shadow-sm border-primary">
          <div class="card-header bg-primary text-white text-center fw-bold fs-5">
            {{ tariff.name }}
          </div>
          <div class="card-body text-center d-flex flex-column justify-content-between">
            <div>
              <div class="display-6 fw-bold text-dark my-2">
                {{ tariff.interest_rate }}%
                <span class="fs-6 text-muted">/ день</span>
              </div>
              <ul class="list-unstyled my-3 text-start px-3">
                <li class="mb-2"><strong>Макс. сумма:</strong> до {{ tariff.max_amount }} руб.</li>
                <li class="mb-2"><strong>Срок займа:</strong> до {{ tariff.term_days }} дней</li>
                <li class="text-success">Без скрытых комиссий</li>
              </ul>
            </div>
            
            <button 
              class="btn btn-outline-primary w-100 mt-3" 
              data-bs-toggle="modal" 
              data-bs-target="#applyLoanModal"
              @click="openApplyModal(tariff)"
            >
              Оформить заём
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="tariffs.length === 0" class="col-12 text-center text-muted">
        Тарифов пока нет.
      </div>
    </div>

    <!-- Модальное окно оформления -->
    <div class="modal fade" id="applyLoanModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Оформление займа: {{ selectedTariff?.name }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          
          <div class="modal-body">
            <div v-if="!currentUser.is_authenticated" class="alert alert-info text-center my-3">
              <h5 class="alert-heading">Вы не вошли в систему</h5>
              <p class="mb-3">Для оформления и получения займа вам нужно войти или создать личный кабинет.</p>
              <button 
                type="button" 
                class="btn btn-primary" 
                data-bs-dismiss="modal" 
                data-bs-toggle="modal" 
                data-bs-target="#loginModal"
              >
                Войти в личный кабинет
              </button>
            </div>

            <form v-else @submit.prevent="submitLoan">
              <div class="mb-3">
                <label class="form-label">Сумма займа (руб.)</label>
                <input 
                  type="number" 
                  step="0.01" 
                  class="form-control" 
                  v-model="loanForm.amount" 
                  :max="selectedTariff?.max_amount" 
                  required
                >
                <small class="text-muted">Максимально: {{ selectedTariff?.max_amount }} руб.</small>
              </div>

              <div class="mb-3">
                <label class="form-label">Отделение для получения наличных</label>
                <select class="form-select" v-model="loanForm.branch">
                  <option value="">Без филиала (онлайн на карту)</option>
                  <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }} ({{ b.city }})</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Скан/фото документа (необязательно)</label>
                <input class="form-control" type="file" ref="loanPictureRef">
              </div>

              <div class="modal-footer px-0 pb-0">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="submit" class="btn btn-success" data-bs-dismiss="modal">Подтвердить и взять заём</button>
              </div>
            </form>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>