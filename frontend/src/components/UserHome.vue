<template>
    <div>
        <h1>User Dashboard</h1>
        
        <div class="container">
            <div class="box">
                <h2>Available Treks</h2>
                <p>{{ available_treks }}</p>
            </div>
            <div class="box">
                <h2>My Booked Treks</h2>
                <p>{{ booked_treks }}</p>
            </div>
            <div class="box">
                <h2>Completed Treks</h2>
                <p>{{ completed_treks }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'UserHome',
    data() {
        return {
            available_treks: 0,
            booked_treks: 0,
            completed_treks: 0
        };
    },
    mounted() {
        this.fetchUserData();
    },
    methods: {
        async fetchUserData() {
            try {
                const token = localStorage.getItem('user_token');
                const response = await axios.get('http://localhost:5000/api/user_home', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                
                this.available_treks = response.data.available_treks;
                this.booked_treks = response.data.booked_treks;
                this.completed_treks = response.data.completed_treks;
            } catch (error) {
                console.error('Error fetching user stats:', error);
            }
        }
    }
}
</script>
