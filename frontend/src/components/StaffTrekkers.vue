<template>
    <header>
        <h1>My Trekkers</h1>
        <p>Users who have registered for your assigned treks.</p>
    </header>
    
    <nav></nav>

    <div>
        <table>
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Booked Treks (Yours)</th>
                    <th>User Status</th>
                </tr>
            </thead>
            
            <tbody>
                <tr v-for="user in trekkers" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    
                    <!-- Loop through the user's booked treks and display them -->
                    <td>
                        <span 
                            v-for="(trek, index) in user.booked_treks" 
                            :key="index" 
                            class="trek-badge"
                        >
                            {{ trek }}
                        </span>
                    </td>
                    
                    <td>
                        <span :class="statusClass(user.status)" class="status-badge">
                            {{ user.status }}
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div v-if="trekkers.length === 0" style="text-align: center; margin-top: 20px; color: #666;">
            No users have booked your treks yet.
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'StaffTrekkers',
    data() {
      return {
        trekkers: [],
      };
    },
    methods: {
        async fetchTrekkers() {
            try {
                const token = localStorage.getItem('staff_token');
                if (!token) return;

                const res = await axios.get('http://localhost:5000/api/get_users_of_staff', {
                    headers: { 
                        Authorization: `Bearer ${token}` 
                    }
                });
                
                this.trekkers = res.data;
            } catch (error) {
                console.error('Error fetching trekkers:', error);
            }
        },
        
        statusClass(status) {
            if (status === 'Active') return 'status-active';
            if (status === 'Inactive') return 'status-inactive';
            if (status === 'Blacklist') return 'status-blacklist';
            return '';
        }
    },
    mounted() {
        this.fetchTrekkers();
    }
}
</script>

<style>
/* Styling for the status badges */
.status-badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.85em;
}
.status-active {
    background-color: #dff0d8;
    color: #3c763d;
}
.status-inactive {
    background-color: #fcf8e3;
    color: #8a6d3b;
}
.status-blacklist {
    background-color: #f2dede;
    color: #a94442;
}

/* Styling for the booked treks badges */
.trek-badge {
    display: inline-block;
    background-color: #e0f2f1;
    color: #00695c;
    padding: 3px 6px;
    margin: 2px;
    border-radius: 4px;
    font-size: 0.85em;
    border: 1px solid #b2dfdb;
}
</style>