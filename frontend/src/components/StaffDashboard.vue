<template>
    <header>
        
            <h1>Welcome, Staff {{ user_details.username }} <button @click="logout()" style="float: right;">Logout</button> </h1>
               
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>
        <button @click="activeTab = 'bookings'" :class="{ active: activeTab === 'bookings'}">Bookings</button>
        <button @click="activeTab = 'trekkers'" :class="{ active: activeTab === 'trekkers'}">Trekkers</button>
        <button @click="activeTab = 'profile'" :class="{ active: activeTab === 'profile'}">Profile</button>
         <button @click="activeTab = 'Summary'" :class="{ active: activeTab === 'Summary'}">Summary</button>

    </nav>
    <main>
        <StaffHome v-if="activeTab === 'home'" :user="user_details" />
        <StaffTreks v-if="activeTab === 'treks'" :user="user_details"/>
        <StaffTrekkers v-if="activeTab === 'trekkers'" :user="user_details"/>
        <StaffBookings v-if="activeTab === 'bookings'" :user="user_details"/>
        <StaffProfile v-if="activeTab === 'profile'" :user="user_details"/>
        <StaffSummary  v-if="activeTab === 'Summary'" :user="user_details" />
    </main>
</template>


<script>
import StaffHome from './StaffHome.vue';
import StaffTreks from './StaffTreks.vue';
import StaffTrekkers from './StaffTrekkers.vue';
import StaffProfile from './StaffProfile.vue';
import StaffBookings from './StaffBookings.vue';
import StaffSummary from './StaffSummary.vue';
export default {
    name: 'StaffDashboard',
    components: {
        StaffHome,
        StaffTreks,
        StaffTrekkers,
        StaffProfile,
        StaffBookings,
        StaffSummary
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
            localStorage.removeItem('staff_token');
            this.$router.push('/');
        },
        async fetchUserDetails() {
            const token = localStorage.getItem('staff_token');
            if (token) {
                try {
                    const response = await fetch('http://localhost:5000/api/staff/profile', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    if (response.ok) {
                        const data = await response.json();
                        this.user_details = data;
                    } else {
                        console.error('Failed to fetch user details');
                    }
                } catch (error) {
                    console.error('Error fetching user details:', error);
                }
            }
        }
    },
    mounted() {
        this.fetchUserDetails();
    }
}
</script>

<style>

</style>