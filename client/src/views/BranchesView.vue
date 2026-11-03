<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const branches = ref([])
const branchPictures = ref([])

const currentUser = ref({ is_authenticated: false, is_staff: false, is_superuser: false })

const branchToAdd = ref({ name: '', city: '', address: '' })
const branchPictureRef = ref()
const branchPictureUrl = ref()

const branchToEdit = ref({})
const editBranchPictureRef = ref()

const activeBranchForAlbum = ref(null)
const albumPictureRef = ref()
const albumPicturePreviewUrl = ref()

const activeModalImage = ref('')

function openImage(url) {
  activeModalImage.value = url
}

function onPictureChange() {
  if (branchPictureRef.value && branchPictureRef.value.files[0]) {
    branchPictureUrl.value = URL.createObjectURL(branchPictureRef.value.files[0])
  }
}

function onAlbumPictureChange() {
  if (albumPictureRef.value && albumPictureRef.value.files[0]) {
    albumPicturePreviewUrl.value = URL.createObjectURL(albumPictureRef.value.files[0])
  }
}

async function fetchData() {
  const [resBranches, resPictures] = await Promise.all([
    axios.get('/api/branches/'),
    axios.get('/api/branch-pictures/')
  ])
  branches.value = resBranches.data
  branchPictures.value = resPictures.data
}

onBeforeMount(async () => {
  try {
    const uRes = await axios.get('/api/users/current/')
    currentUser.value = uRes.data
  } catch (e) {}
  await fetchData()
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
  await fetchData()
}

async function onBranchDelete(item) {
  if (!confirm('Удалить этот филиал со всеми фото?')) return
  await axios.delete(`/api/branches/${item.id}/`)
  await fetchData()
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
  await fetchData()
}

function openAlbum(branch) {
  activeBranchForAlbum.value = branch
  albumPicturePreviewUrl.value = null
  if (albumPictureRef.value) albumPictureRef.value.value = ''
}

async function onAddPhotoToAlbum() {
  if (!albumPictureRef.value || !albumPictureRef.value.files[0]) {
    alert('Выберите файл с фотографией!')
    return
  }
  const formData = new FormData()
  formData.append('branch', activeBranchForAlbum.value.id)
  formData.append('picture', albumPictureRef.value.files[0])
  await axios.post('/api/branch-pictures/', formData)
  albumPicturePreviewUrl.value = null
  if (albumPictureRef.value) albumPictureRef.value.value = ''
  await fetchData()
}

async function onDeletePhotoFromAlbum(pictureId) {
  if (!confirm('Удалить эту фотографию из альбома?')) return
  await axios.delete(`/api/branch-pictures/${pictureId}/`)
  await fetchData()
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Наши филиалы и отделения</h2>
      <span v-if="currentUser.is_staff || currentUser.is_superuser" class="badge bg-secondary">
        Режим управления персоналом
      </span>
    </div>

    <div v-if="currentUser.is_staff || currentUser.is_superuser" class="card p-3 my-3 bg-light shadow-sm">
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
          <button class="btn btn-primary w-100" type="submit">+</button>
        </div>
        <div class="col-12 mt-2" v-if="branchPictureUrl">
          <span class="me-2 text-muted">Предпросмотр:</span>
          <img :src="branchPictureUrl" style="max-height: 50px; border-radius: 4px;" />
        </div>
      </form>
    </div>

    <div v-if="!currentUser.is_staff && !currentUser.is_superuser" class="row g-4 my-2">
      <div class="col-md-4 col-sm-6" v-for="item in branches" :key="item.id">
        <div class="card h-100 shadow-sm border-0 bg-white">
          <img 
            :src="item.picture || '/default_loan.png'" 
            class="card-img-top p-3" 
            style="height: 180px; object-fit: contain; background: #f8f9fa; cursor: pointer;"
            data-bs-toggle="modal" 
            data-bs-target="#imageModal" 
            @click="openImage(item.picture || '/default_loan.png')" 
            title="Нажмите для увеличения"
          />
          <div class="card-body d-flex flex-column justify-content-between">
            <div>
              <h5 class="card-title text-primary fw-bold">{{ item.name }}</h5>
              <p class="card-text text-muted mb-1"><strong>Город:</strong> {{ item.city }}</p>
              <p class="card-text text-muted"><strong>Адрес:</strong> {{ item.address }}</p>
            </div>
            <button 
              class="btn btn-outline-info w-100 mt-3" 
              data-bs-toggle="modal" 
              data-bs-target="#albumModal" 
              @click="openAlbum(item)"
            >
              Фотоальбом отделения ({{ branchPictures.filter(p => p.branch === item.id).length }})
            </button>
          </div>
        </div>
      </div>
      <div v-if="branches.length === 0" class="col-12 text-center text-muted">
        Филиалов пока нет.
      </div>
    </div>

    <table v-else class="table table-striped mt-3 align-middle">
      <thead>
        <tr>
          <th>ID</th>
          <th>Логотип / Фото</th>
          <th>Название</th>
          <th>Город</th>
          <th>Адрес</th>
          <th style="width: 290px;">Действия</th>
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
              class="btn btn-info btn-sm me-2 text-white" 
              data-bs-toggle="modal" 
              data-bs-target="#albumModal" 
              @click="openAlbum(item)"
            >
              Альбом ({{ branchPictures.filter(p => p.branch === item.id).length }})
            </button>
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
      </tbody>
    </table>

    <!-- Модальное окно альбома -->
    <div class="modal fade" id="albumModal" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Фотоальбом филиала: {{ activeBranchForAlbum?.name }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <!-- Загрузка фото видна только персоналу -->
            <div v-if="currentUser.is_staff || currentUser.is_superuser" class="card p-3 mb-4 bg-light">
              <h6>Добавить фотографию в альбом:</h6>
              <div class="row g-2 align-items-center">
                <div class="col-md-9">
                  <input class="form-control" type="file" ref="albumPictureRef" @change="onAlbumPictureChange">
                </div>
                <div class="col-md-3">
                  <button class="btn btn-primary w-100" @click="onAddPhotoToAlbum">Загрузить</button>
                </div>
                <div class="col-12 mt-2" v-if="albumPicturePreviewUrl">
                  <span class="me-2 text-muted">Предпросмотр:</span>
                  <img :src="albumPicturePreviewUrl" style="max-height: 60px; border-radius: 4px;" />
                </div>
              </div>
            </div>

            <!-- Галерея фото -->
            <div class="row g-3">
              <div 
                class="col-md-4 col-sm-6 text-center" 
                v-for="pic in branchPictures.filter(p => p.branch === activeBranchForAlbum?.id)" 
                :key="pic.id"
              >
                <div class="card p-2 shadow-sm h-100">
                  <img 
                    :src="pic.picture" 
                    class="card-img-top" 
                    style="height: 140px; object-fit: cover; cursor: pointer; border-radius: 4px;" 
                    data-bs-toggle="modal" 
                    data-bs-target="#imageModal" 
                    @click="openImage(pic.picture)"
                  />
                  <!-- Удаление фото доступно только персоналу -->
                  <div v-if="currentUser.is_staff || currentUser.is_superuser" class="card-body p-2 d-flex flex-column justify-content-end">
                    <button class="btn btn-outline-danger btn-sm w-100" @click="onDeletePhotoFromAlbum(pic.id)">Удалить фото</button>
                  </div>
                </div>
              </div>
            </div>

            <div 
              v-if="branchPictures.filter(p => p.branch === activeBranchForAlbum?.id).length === 0" 
              class="text-center text-muted my-4"
            >
              В альбоме этого филиала пока нет фотографий.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть альбом</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования филиала -->
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

    <!-- Модальное окно просмотра увеличенного фото -->
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