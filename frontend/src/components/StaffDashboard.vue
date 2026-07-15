<template>
    <header>
        
            <h1>Welcome, Staff {{ user_details.username }} <button @click="logout()" style="float: right;">Logout</button> </h1>
               
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>
        <button @click="activeTab = 'bookings'" :class="{ active: activeTab === 'bookings'}">Bookings</button>
        <button @click="activeTab = 'trekkers'" :class="{ active: activeTab === 'trekkers'}">Trekkers</button>
        <button @click="activeTab = 'profile'" :class="{ active: activeTab === 'profile'}">Edit Profile</button>
        <button @click="activeTab = 'Summary'" :class="{ active: activeTab === 'Summary'}">Summary</button>

    </nav>
    <main>
        <StaffHome v-if="activeTab === 'home'"/>
        <StaffTreks v-if="activeTab === 'treks'"/>
        <StaffTrekkers v-if="activeTab === 'trekkers'"/>
        <StaffBookings v-if="activeTab === 'bookings'"/>
        <StaffProfile v-if="activeTab === 'profile'"/>
        <StaffSummary  v-if="activeTab === 'Summary'" />
    </main>
</template>


<script>
import StaffHome from './StaffHome.vue';
import StaffTreks from './StaffTreks.vue';
import StaffTrekkers from './StaffTrekkers.vue';
import StaffProfile from './EditProfile.vue';
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
                    const response = await fetch('http://localhost:5000/api/profile', {
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