<template>
    <div v-if="!isLoggedIn">
        <StaffLogin @logged-in="handleStaffLogin" />
    </div>
    <div v-else>
        <StaffDashboard />
    </div>
    

</template>


<script>
import StaffLogin from '@/components/StaffLogin.vue';
import StaffDashboard from '@/components/StaffDashboard.vue';

export default {
  name: 'StaffView',
  components: {
    StaffLogin,
    StaffDashboard
  },
  data() {
    return {
        isLoggedIn: false,
    };
  },
  methods: {
    handleStaffLogin() {
        this.isLoggedIn = true;
    },
    cancel() {
      this.$router.push('/');
    }
    
  },
};


</script>

<style>

</style>