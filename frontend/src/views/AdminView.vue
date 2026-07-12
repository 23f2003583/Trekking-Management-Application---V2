<template>
    <div>
        
        <div v-if="!isLoggedIn">
            <AdminLogin @logged-in="handleAdminLogin" />
        </div>
        <div v-else>
            <AdminDashboard />
        </div>
    </div>

</template>



<script>
import AdminLogin from '@/components/AdminLogin.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';




export default {
  name: 'AdminView',
  components: {
    AdminLogin,
    AdminDashboard
  },
  data() {
    return {
        isLoggedIn: false,
    };
  },
  methods: {
    handleAdminLogin() {
        this.isLoggedIn = true;
    },
    cancel() {
      this.$router.push('/');
    }
    
  },
};

</script>