<template>
 <header>
        
    <h1>Treks</h1>
    <p>This is the Treks page</p>
    
        </header>
    <nav>
        
    </nav>
    <main>
        <CreateTrek v-if="activeTab === 'create_trek'" 
        @registered="TrekAdded" 
        @cancel="activeTab = 'list'" />
        <EditTrek v-if="activeTab === 'edit_trek'"
        :trek="selectedTrek"
        @updated="trekUpdated"
        @cancel="activeTab = 'list'" />
    </main>
    <div v-if="activeTab === 'list'">
        <button @click="activeTab = 'create_trek'" :class="{ active: activeTab === 'create_trek'}" style="float: right;">Create Trek</button>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <!-- <th>Description</th> -->
                    <th>Available Slots</th>
                    <!-- <th>Staff ID</th> -->
                    <th>Staff Name</th>
                    <th>Price</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Status</th>
                    <th>Actions</th> </tr>
            </thead>
            
            <tbody>
                <tr v-for="trek in treks" :key="trek.id">
                    <td>{{ trek.id }}</td>
                    <td>{{ trek.name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>{{ trek.difficulty }}</td>
                    <td>{{ trek.duration }}</td>
                    <!-- <td>{{ trek.description }}</td> -->
                    <td>{{ trek.available_slots }}</td>
                    <!-- <td>{{ trek.staff_id }}</td> -->
                    <td>{{ trek.staff_name }}</td>
                    <td>{{ trek.price }}</td>
                    <td>{{ trek.start_date }}</td>
                    <td>{{ trek.end_date }}</td>
                    <td><button @click="updateTrekStatus(trek.id)">
                             {{ trek.status }}
                        </button></td>
                    <td>
                        <button @click="deleteTrek(trek.id)" style="margin-left: 10px; color: red;">
                            {{ trek.is_deleted ? 'Deleted' : 'Delete' }}
                        </button>
                        <button @click="openEditForm(trek)">
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
import CreateTrek from './CreateTrek.vue';
import EditTrek from './EditTrek.vue';
export default {
    name: 'AdminTreks',
    components: {
        CreateTrek,
        EditTrek
    },
    data() {
      return {
        activeTab: 'list', 
        treks: [],
        selectedTrek: null
      };
    
    },
    methods: {
        openEditForm(trek) {
            this.selectedTrek = trek;
            this.activeTab = 'edit_trek';
        },
        TrekAdded() {
        this.activeTab = 'list'; 
        this.fetchTreks();      
        },
        trekUpdated() {
            this.activeTab = 'list'; 
            this.fetchTreks();      
        },
        async fetchTreks() {
            const token = localStorage.getItem('admin_token');
            const res=await axios.get('http://localhost:5000/api/get_treks', {
                headers: {
                    Authorization: `Bearer ${token}` 
                }
            });
            this.treks = res.data;
        
        },
        async updateTrekStatus(trekId) {
            const token = localStorage.getItem('admin_token');
            try {
                await axios.put(`http://localhost:5000/api/update_treks/${trekId}/status`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}` 
                    }
                });
                this.fetchTreks(); 
            } catch (error) {
                console.error('Error updating trek status:', error);
            }
        },
        async deleteTrek(trekId) {
            const token = localStorage.getItem('admin_token');
            try {
                await axios.delete(`http://localhost:5000/api/delete_trek/${trekId}`, {
                    headers: {
                        Authorization: `Bearer ${token}` 
                    }
                });
                this.fetchTreks(); 
            } catch (error) {
                console.error('Error deleting trek:', error);
            }
        }
    },
    mounted() {
        this.fetchTreks();
    }
}

</script>

<style>

</style>