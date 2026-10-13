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
        <div class="navbar-nav">
          <RouterLink class="nav-link" to="/branches">Филиалы</RouterLink>
          <RouterLink class="nav-link" to="/tariffs">Тарифы</RouterLink>
          <RouterLink class="nav-link" to="/loans">Займы</RouterLink>
          <RouterLink class="nav-link" to="/payments">Платежи</RouterLink>
          <RouterLink class="nav-link" to="/users">Пользователи</RouterLink>
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
