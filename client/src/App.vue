<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, computed, onBeforeMount} from 'vue'
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
})

</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container">
        <span class="navbar-brand fw-bold text-info">Синий Крест Давида</span>

        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          
          <ul class="navbar-nav">
            <li class="nav-item"><RouterLink class="nav-link" to="/branches">Филиалы</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/tariffs">Тарифы</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/loans">Займы</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/payments">Платежи</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/users">Пользователи</RouterLink></li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
              </ul>
            </li>
          </ul>

        </div>
      </div>
    </nav>

    <div class="container">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.nav-link.router-link-active {
  color: #0dcaf0 !important;
  font-weight: bold;
}
</style>
