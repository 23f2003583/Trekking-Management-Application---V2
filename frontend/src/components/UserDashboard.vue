<template>
    <header>
        
            <h1>Welcome,{{ user_details.username }} <button @click="logout()" style="float: right;">Logout</button>    </h1>
        </header>
    <nav>
        <button @click="activeTab = 'home'" :class="{ active: activeTab === 'home'}">Dashboard</button>
        <button @click="activeTab = 'treks'" :class="{ active: activeTab === 'treks'}">Treks</button>
        <button @click="activeTab = 'bookings'" :class="{ active: activeTab === 'bookings'}">Bookings</button>
        <button @click="activeTab = 'profile'" :class="{ active: activeTab === 'profile'}">Edit Profile</button>
        <button @click="activeTab = 'summary'" :class="{ active: activeTab === 'summary'}">Summary</button>
        <button @click="activeTab = 'search'" :class="{ active: activeTab === 'search'}" style="float: right;">search</button>

     </nav>
    <main>
        <UserHome v-if="activeTab === 'home'" />       
        <UserBookings v-if="activeTab === 'bookings'" />
        <UserTreks v-if="activeTab === 'treks'" />
        <UserSummary v-if="activeTab === 'summary'" />
        <Profile v-if="activeTab === 'profile'" />
        <UserSearch v-if="activeTab === 'search'" />
    </main>
</template>


<script>
import UserBookings from './UserBookings.vue';
import UserTreks from './UserTreks.vue';
import UserSummary from './UserSummary.vue';
import UserSearch from './UserSearch.vue';
import UserHome from './UserHome.vue';
import Profile from './EditProfile.vue';

export default {
    name: 'UserDashboard',
    components: {
        UserBookings,
        UserTreks,
        UserSummary,
        UserSearch,
        UserHome,
        Profile
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
            localStorage.removeItem('user_token');
            this.$router.push('/');
        },
        async fetchUserDetails() {
            const token = localStorage.getItem('user_token');
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
    mounted(){
        this.fetchUserDetails();
    }
}
</script>
