<template>
    <header>
        <h1>My Bookings</h1>
        <p>This is the Booking page</p>
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
                    <th>Description</th>
                    <th>Staff Name</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Trek Status</th>
                    <th>Booking Status</th>
                    <th>Actions</th> 
                </tr>
            </thead>
            
            <tbody>
                <tr v-for="booking in bookings" :key="booking.booking_id">
                    <td>{{ booking.booking_id }}</td>
                    <td>{{ booking.name }}</td>
                    <td>{{ booking.location }}</td>
                    <td>{{ booking.booking_date }}</td>
                    <td>{{ booking.duration }}</td>
                    <td>{{ booking.description }}</td>
                    <td>{{ booking.staff_name }}</td>
                    <td>{{ booking.start_date }}</td>
                    <td>{{ booking.end_date }}</td>
                    <td>{{ booking.status }}</td>
                    <td><button>{{ booking.booking_status }}</button></td>
                    <td>
                        <button 
                            v-if="booking.booking_status !== 'Cancelled' && booking.booking_status !== 'Completed'"
                            @click="Cancel_Booking(booking.booking_id)"
                            style="background-color: #ff4c4c; color: white; border: none; padding: 4px 8px; cursor: pointer; border-radius: 4px;"
                        >
                            Cancel
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
    name: 'UserBookings',
    data() {
      return {
        bookings: [],
      };
    },
    methods: {
        async fetchbooking() {
            try {
                const token = localStorage.getItem('user_token');
                
                const res = await axios.get('http://localhost:5000/api/get_bookings_of_user',  { 
                    headers: { Authorization: `Bearer ${token}` } 
                });
                this.bookings = res.data;
            } catch (error) {
                console.error('Error fetching bookings:', error);
            }
        },
        
        async Cancel_Booking(bookingId) {
            if (!confirm("Are you sure you want to cancel this booking?")) {
                return;
            }

            try {
                const token = localStorage.getItem('user_token'); 
                if (!token) return;

                await axios.delete(`http://localhost:5000/api/cancel_bookings/${bookingId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                
                alert('Booking cancelled successfully!');
                
                this.fetchbooking();
                
            } catch (error) {
                console.error(error);
                const errorMsg = error.response?.data?.message || 'Error cancelling booking.';
                alert(errorMsg);
            }
        }
    },
    mounted() {
        this.fetchbooking();
    }
}
</script>

