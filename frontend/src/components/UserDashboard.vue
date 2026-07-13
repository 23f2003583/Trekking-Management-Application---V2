<template>
    <header>
        
            <h1>Welcome, <button @click="logout()" style="float: right;">Logout</button>    </h1>
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>
        <button @click="activeTab = 'bookings'" :class="{ active: activeTab === 'bookings'}">Bookings</button>
        <button @click="activeTab = 'analysis'" :class="{ active: activeTab === 'analysis'}">Analysis</button>
        <button @click="activeTab = 'summary'" :class="{ active: activeTab === 'summary'}">Summary</button>
        <button @click="activeTab = 'search'" :class="{ active: activeTab === 'search'}" style="float: right;">search</button>

     </nav>
    <main>
        <UserBookings v-if="activeTab === 'bookings'" />
        <UserTreks v-if="activeTab === 'treks'" />
        <UserSummary v-if="activeTab === 'summary'" />
        <UserSearch v-if="activeTab === 'search'" />
    </main>
</template>


<script>
import UserBookings from './UserBookings.vue';
import UserTreks from './UserTreks.vue';
import UserSummary from './UserSummary.vue';
import UserSearch from './UserSearch.vue';
export default {
    name: 'UserDashboard',
    components: {
        UserBookings,
        UserTreks,
        UserSummary,
        UserSearch
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
            localStorage.removeItem('user_token');
            this.$router.push('/');
        }
    }
}
</script>

<style>

</style>