<template>
    <div>
        <h1>Users List</h1>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Status</th>
                    <th>Actions</th> 
                </tr>
            </thead>
            
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.name }}</td>

                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td><button @click="updateUserStatus(user.id)">
                             {{ user.status }}
                        </button></td>
                    <td>
                        <button @click="deleteUser(user.id)" style="margin-left: 10px; color: red;">
                            {{ user.is_deleted ? 'Deleted' : 'Delete' }}
                        </button>
                        
                    </td>
                </tr>
            </tbody>
        </table>
        
    </div>
</template>


<script>
import axios from 'axios';

export default {
    name: 'AdminUsers',
    data() {
        return {
            users :[] 
        };
    },
    
    
    methods: {
        
        async fetchUsers() {
            const token = localStorage.getItem('admin_token');
            const res=await axios.get('http://localhost:5000/api/get_users', {
                headers: {
                    Authorization: `Bearer ${token}` 
                }
            });
            this.users = res.data;
        },
        async updateUserStatus(userId) {
            const token = localStorage.getItem('admin_token');
            try {
                await axios.put(`http://localhost:5000/api/users/${userId}/status`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}` 
                    }
                });
                
                this.fetchUsers();
            } catch (error) {
                console.error("Failed to update user status:", error.response ? error.response.data : error);
            }
        },
        
        async deleteUser(userId) {
            if (!confirm("Are you sure you want to delete this user?")) {
                return; 
            }

            const token = localStorage.getItem('admin_token');
            try {
                await axios.delete(`http://localhost:5000/api/delete_users/${userId}`, {
                    headers: {
                        Authorization: `Bearer ${token}` 
                    }
                });
                
                this.fetchUsers();
            } catch (error) {
                console.error("Failed to delete user:", error.response ? error.response.data : error);
            }
        }

    },
    mounted() {
        this.fetchUsers();
}
}



</script>