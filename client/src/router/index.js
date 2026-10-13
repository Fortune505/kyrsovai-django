import { createRouter, createWebHistory } from 'vue-router'
import BranchesView from '../views/BranchesView.vue'
import TariffsView from '../views/TariffsView.vue'
import LoansView from '../views/LoansView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import UsersView from '../views/UsersView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/branches'
    },
    {
      path: '/branches',
      name: 'branches',
      component: BranchesView
    },
    {
      path: '/tariffs',
      name: 'tariffs',
      component: TariffsView
    },
    {
      path: '/loans',
      name: 'loans',
      component: LoansView
    },
    {
      path: '/payments',
      name: 'payments',
      component: PaymentsView
    },
    {
      path: '/users',
      name: 'users',
      component: UsersView
    }
  ]
})

export default router
