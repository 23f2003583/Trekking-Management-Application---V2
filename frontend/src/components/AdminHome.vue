<template>
    <div>
        <h1>Admin Home</h1>
        <p></p>
    </div>
    <div class="container">
        <div class="box">
            <h2>Trek Count: {{ trek_count }}</h2>
        </div>
        <div class="box">
            <h2>User Count: {{ user_count }}</h2>
            <p></p>
        </div>
        <div class="box">
            <h2>Staff Count: {{ staff_count }}</h2>
        </div>
        <div class="box">
            <h2>Booking Count: {{ booking_count }}</h2>
        </div>
        </div>

        </template>

<script>
import axios from 'axios';
export default {
    name: 'AdminHome',
    data() {
        return {
            trek_count: 0,
            user_count: 0,
            staff_count: 0,
            booking_count: 0
        };
    },
    mounted() {
        this.fetchAdminData();
    },
    methods: {
        async fetchAdminData() {
            try {
                const token = localStorage.getItem('admin_token');
                const response = await axios.get('http://localhost:5000/api/admin_home', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                const { trek_count, user_count, staff_count, booking_count } = response.data;
                this.trek_count = trek_count;
                this.user_count = user_count;
                this.staff_count = staff_count;
                this.booking_count = booking_count;
            } catch (error) {
                console.error('Error fetching admin data:', error);
            }
        }
    }
}
</script>
