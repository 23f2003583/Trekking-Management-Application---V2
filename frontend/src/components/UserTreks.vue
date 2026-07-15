<template>
    <header>
        <h1>Treks</h1>
        <p>This is the Treks page</p>
    </header>
    
    <nav></nav>

    <div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Description</th>
                    <th>Available Slots</th>
                    <th>Staff ID</th>
                    <th>Staff Name</th>
                    <th>Price</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Status</th>
                    <th>Actions</th> 
                </tr>
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
                        <td>{{ trek.staff_id }}</td>
                        <td>{{ trek.staff_name }}</td>
                        <td>{{ trek.price }}</td>
                        <td>{{ trek.start_date }}</td>
                        <td>{{ trek.end_date }}</td>
                        <td><button>{{ trek.status }}</button></td>
                        <td>
                            <button 
                                @click="Book_Trek(trek.id)" 
                                :disabled="!!trek.my_booking_status">
                                {{ trek.my_booking_status ? 'Booked' : 'Book Trek' }}
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
    name: 'UserTreks',
    data() {
      return {
        treks: [],
      };
    },
    computed: {
        activeTreks() {
            return this.treks.filter(trek => trek.is_deleted !== true);
        }
    },
    methods: {
        async fetchTreks() {
            try {
                const token = localStorage.getItem('user_token');
                const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
                
                const res = await axios.get('http://localhost:5000/api/get_treks', config);
                this.treks = res.data;
            } catch (error) {
                console.error('Error fetching treks:', error);
            }
        },
        
        async Book_Trek(trekId) {
            try {
                const token = localStorage.getItem('user_token'); 
                
                if (!token) {
                    alert("Error: You are not logged in, or the token is missing!");
                    return; 
                }

                await axios.post(`http://localhost:5000/api/book_trek/${trekId}`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                
                alert('Trek booked successfully!');
                this.fetchTreks();
                
            } catch (error) {
                console.error(error);
                const errorMsg = error.response?.data?.message || 'Error booking trek.';
                alert(errorMsg);
            }
        }
    },
    mounted() {
        this.fetchTreks();
    }
}
</script>
