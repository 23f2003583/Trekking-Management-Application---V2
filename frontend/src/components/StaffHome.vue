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


        <h1>Recent Bookings</h1>
        <p></p>
</template>

<script>
import axios from 'axios';

export default {
    name: 'StaffHome',
    data() {
        return {
            trek_count: 0,
            user_count: 0,
            staff_count: 0,
            booking_count: 0
        };
    },
    // Optional: Add a mounted hook later when you are ready to fetch the real data for the staff!
}
</script>
