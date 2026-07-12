<template>
    <header>
        
            <h1>Welcome,</h1>
            <button @click="logout()">Logout</button>    
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>
        <button @click="activeTab = 'bookings'" :class="{ active: activeTab === 'bookings'}">Bookings</button>
        <button @click="activeTab = 'analysis'" :class="{ active: activeTab === 'analysis'}">Analysis</button>
    </nav>
    <main>
        <UserBookings v-if="activeTab === 'bookings'" />
        <UserTreks v-if="activeTab === 'treks'" />
    </main>
    <div></div>
    <h1>User Dashboard</h1>
    <p>This is the Dashboard page</p>
</template>


<script>
import UserBookings from './UserBookings.vue';
import UserTreks from './UserTreks.vue';
export default {
    name: 'UserDashboard',
    components: {
        UserBookings,
        UserTreks
    },
    data() {
      return {
        activeTab: 'dashboard', 
        user_details: {
          // Add any data properties you need here
        }
      };
    },
    methods: {
        logout() {
            localStorage.removeItem('user_token');
            this.$router.push('/');
        }
    }
}
</script>

<style>

</style>