<template>
    <header>
        <h1>My Assigned Bookings</h1>
        <p>Manage bookings for your assigned treks.</p>
    </header>
    
    <nav></nav>

    <div>
        <table>
            <thead>
                <tr>
                    <th>Booking ID</th>
                    <th>Trek Name</th>
                    <th>Location</th>
                    <th>Booking Date</th>
                    <th>Duration</th>
                    <th>Trekker Name</th> 
                    <th>Trekker Email</th> 
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Trek Status</th>
                    <th>Booking Status</th>
                </tr>
            </thead>
            
            <tbody>
                <tr v-for="booking in bookings" :key="booking.booking_id">
                    <td>{{ booking.booking_id }}</td>
                    <td>{{ booking.name }}</td>
                    <td>{{ booking.location }}</td>
                    <td>{{ booking.booking_date }}</td>
                    <td>{{ booking.duration }}</td>
                    
                    <td>{{ booking.user_name }} </td>
                    <td>{{ booking.email }}</td>
                    
                    <td>{{ booking.start_date }}</td>
                    <td>{{ booking.end_date }}</td>
                    <td>{{ booking.status }}</td>
                    <td>
                        <button 
                            @click="Update_Status(booking.booking_id)"
                            >
                            {{ booking.booking_status }}
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
    name: 'StaffBookings',
    data() {
      return {
        bookings: [],
      };
    },
    methods: {
        async fetchbooking() {
            try {
                const token = localStorage.getItem('staff_token');
                const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
                
                const res = await axios.get('http://localhost:5000/api/get_bookings_of_staff', config);
                this.bookings = res.data;
            } catch (error) {
                console.error('Error fetching bookings:', error);
            }
        },
        
        async Update_Status(bookingId) {
            try {
                const token = localStorage.getItem('staff_token'); 
                if (!token) return;

                await axios.put(`http://localhost:5000/api/update_booking_status/${bookingId}/status`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                
                this.fetchbooking();
                
            } catch (error) {
                console.error(error);
                const errorMsg = error.response?.data?.message || 'Error updating booking.';
                alert(errorMsg);
            }
        }
    },
    mounted() {
        this.fetchbooking();
    }
}
</script>
