<template>
    <header>
        
            <h1>Welcome, Admin        
<button @click="logout()" style="float: right;">Logout</button> </h1>
               
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'users'" :class="{ active: activeTab === 'users'}">Users</button>
        <button @click="activeTab = 'staffs'" :class="{ active: activeTab === 'staffs'}">Staffs</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>       
        <button @click="activeTab = 'booking'" :class="{ active: activeTab === 'booking'}">Bookings</button>
        <button @click="activeTab = 'summary'" :class="{ active: activeTab === 'summary'}">Summary</button>
        <button @click="activeTab = 'search'" :class="{ active: activeTab === 'search'}" style="float: right ">search</button>

    </nav>
    <main>
        <AdminHome v-if="activeTab === 'home'" />
        <AdminUsers v-if="activeTab === 'users'" />
        <AdminStaffs v-if="activeTab === 'staffs'" />
        <AdminTreks v-if="activeTab === 'treks'" />
        <AdminSummary v-if="activeTab== 'summary'" />
        <AdminBooking v-if="activeTab== 'booking'"/>
        <AdminSearch v-if="activeTab== 'search'"/>

    </main>
</template>


<script>
import AdminHome from './AdminHome.vue';
import AdminUsers from './AdminUsers.vue';
import AdminStaffs from './AdminStaffs.vue';
import AdminTreks from './AdminTreks.vue';
import AdminSummary from './AdminSummary.vue';  
import AdminBooking from './AdminBooking.vue';
import AdminSearch from './AdminSearch.vue';

export default {
    name: 'AdminDashboard',
    components: {
        AdminHome,
        AdminUsers,
        AdminStaffs,
        AdminTreks,
        AdminSummary,
        AdminBooking,
        AdminSearch
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