<template>
 <header>
        
    <h1>Staffs</h1>
    <p>This is the Staffs page</p>
        </header>
    <nav>
        
    </nav>
    <main>
        <CreateStaff 
        v-if="activeTab === 'create_staff'" 
        @registered="StaffAdded" 
        @cancel="activeTab = 'list'" />
        <EditStaff 
        v-if="activeTab === 'edit_staff'"
        :staff="selectedStaff"
        @updated="StaffUpdated"
        @cancel="activeTab = 'list'" />
    </main>
    <div v-if="activeTab === 'list'">
            <button @click="activeTab = 'create_staff'" :class="{ active: activeTab === 'create_staff'}" style="float: right;">Create Staff</button>

        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Treks</th>
                    <th>Status</th>
                    <th>Actions</th> </tr>
            </thead>
            
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                        <ul>
                            <li v-for="trek in user.treks" :key="trek.id">
                                {{ trek.name }}
                            </li>
                        </ul>
                    </td>
                    <td><button @click="updateUserStatus(user.id)">
                             {{ user.status }}
                        </button></td>
                    <td>
                        <button @click="deleteUser(user.id)" style="margin-left: 10px; color: red;">
                            {{ user.is_deleted ? 'Deleted' : 'Delete' }}
                        </button>
                        <button @click="openEditForm(user)">
                            Edit
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        
    </div>
    
</template>


<script>
import axios from 'axios';
import CreateStaff from './CreateStaffs.vue';
import EditStaff from './EditStaff.vue';
export default {
    name: 'AdminStaffs',
    components: {
        CreateStaff,
        EditStaff
    },
    data() {
      return {
        activeTab: 'list', 
        users: [],
        selectedStaff: null
      };
    
    },
    methods: {
        StaffAdded() {
        this.activeTab = 'list'; 
        this.fetchStaffs();      
        },
        openEditForm(staff) {
            this.selectedStaff = staff;
            this.activeTab = 'edit_staff';
        },
        StaffUpdated() {
            this.activeTab = 'list'; 
            this.fetchStaffs();      
        },
        async fetchStaffs() {
            const token = localStorage.getItem('admin_token');
            const res=await axios.get('http://localhost:5000/api/get_staffs', {
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
                
                this.fetchStaffs();
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
                
                this.fetchStaffs();
            } catch (error) {
                console.error("Failed to delete user:", error.response ? error.response.data : error);
            }
        }
},
    mounted() {
        this.fetchStaffs();
    }
}

</script>
