<template>
    <div>
        <h1>Staff Home</h1>
        
        <div class="container">
            <div class="box">
                <h2>Assigned Treks: {{ assigned_trek_count }}</h2>
            </div>
        </div>

        <div v-if="treks_user_counts.length > 0">
            <h3>Registered Users per Trek</h3>
            <table >
                <thead>
                    <tr>
                        <th >Trek Name</th>
                        <th >User Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="trek in treks_user_counts" :key="trek.trek_name">
                        <td >{{ trek.trek_name }}</td>
                        <td>{{ trek.user_count }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No trekking data available.</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'StaffHome',
    data() {
        return {
            assigned_trek_count: 0,
            treks_user_counts: [] 
        };
    },
    mounted() {
        this.fetchStaffData();
    },
    methods: {
        async fetchStaffData() {
            try {
                const token = localStorage.getItem('staff_token');
                const response = await axios.get('http://localhost:5000/api/staff_home', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                this.assigned_trek_count = response.data.assigned_trek_count;
                this.treks_user_counts = response.data.treks_user_counts;
            } catch (error) {
                console.error('Error fetching staff data:', error);
            }
        }
    }
}
</script>

