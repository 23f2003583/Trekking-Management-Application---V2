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
                    
                    <td>
                        <ul>
                            <li v-for="trek in user.booked_treks" :key="trek.id" >
                                {{ trek }}
                            </li>
                        </ul>
                    </td>
                    
                    <td>
                        <button :class="statusClass(user.status)" class="status-badge">
                            {{ user.status }}
                        </button>
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

</style>