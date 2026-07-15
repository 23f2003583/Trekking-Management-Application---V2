<template>
 <header>
        
    <h1>Treks</h1>
    <p>This is the Treks page</p>
    
        </header>
    <nav>
        
    </nav>
    <main>
       
        <EditTrek v-if="activeTab === 'edit_trek'"
        :trek="selectedTrek"
        @updated="trekUpdated"
        @cancel="activeTab = 'list'" />
    </main>
    <div v-if="activeTab === 'list'">        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Available Slots</th>
                    <th>Price</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Status</th>
                    <th>Actions</th> </tr>
            </thead>
            
            <tbody>
                <tr v-for="trek in activeTreks" :key="trek.id">
                    
                        <td>{{ trek.id }}</td>
                        <td>{{ trek.name }}</td>
                        <td>{{ trek.location }}</td>
                        <td>{{ trek.difficulty }}</td>
                        <td>{{ trek.duration }}</td>
                        <td>{{ trek.description }}</td>
                        <td>{{ trek.available_slots }}</td>
                        <td>{{ trek.price }}</td>
                        <td>{{ trek.start_date }}</td>
                        <td>{{ trek.end_date }}</td>
                        <td><button @click="updateTrekStatus(trek.id)">
                                {{ trek.status }}
                            </button></td>
                        <td>
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
import EditTrek from './EditTrek.vue';
export default {
    name: 'StaffTreks',
    components: {
        EditTrek
    },
    props: {
        user: {
            type: Object,
            required: true
        }
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
        trekUpdated() {
            this.activeTab = 'list'; 
            this.fetchTreks();      
        },
        async fetchTreks() {
            try {
                const token = localStorage.getItem('staff_token');
                
                if (!token) {
                    console.error("No staff token found! Please log in.");
                    return; 
                }

                const res = await axios.get('http://localhost:5000/api/get_treks_of_staff', {
                    headers: {
                        Authorization: `Bearer ${token}` 
                    }
                });
                this.treks = res.data;
            } catch (error) {
                console.error("Failed to fetch staff treks:", error.response?.data?.message || error);
            }
        },
        async updateTrekStatus(trekId) {
            const token = localStorage.getItem('staff_token');
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
        
    }
        
    },
    mounted() {
        this.fetchTreks();
    },
    computed: {
        activeTreks() {
            return this.treks.filter(trek => !trek.is_deleted);
        }
    }
}

</script>

