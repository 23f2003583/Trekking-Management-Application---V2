<template>
    <header>
        
            <h1>Welcome, Admin <button @click="logout()" style="float: right;">Logout</button> </h1>
               
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'users'" :class="{ active: activeTab === 'users'}">Users</button>
        <button @click="activeTab = 'staffs'" :class="{ active: activeTab === 'staffs'}">Staffs</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>
    </nav>
    <main>
        <AdminHome v-if="activeTab === 'home'" />
        <AdminUsers v-if="activeTab === 'users'" />
        <AdminStaffs v-if="activeTab === 'staffs'" />
        <AdminTreks v-if="activeTab === 'treks'" />
    </main>
</template>


<script>
import AdminHome from './AdminHome.vue';
import AdminUsers from './AdminUsers.vue';
import AdminStaffs from './AdminStaffs.vue';
import AdminTreks from './AdminTreks.vue';
export default {
    name: 'AdminDashboard',
    components: {
        AdminHome,
        AdminUsers,
        AdminStaffs,
        AdminTreks
    },
    data() {
      return {
        activeTab: 'home', 
        user_details: {
          // Add any data properties you need here
        }
      };
    },
    methods: {
        logout() {
            localStorage.removeItem('admin_token');
            this.$router.push('/');
        }
    }
}
</script>

<style>

</style>