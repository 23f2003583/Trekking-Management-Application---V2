<template>
  <div class="trek-register">
    <button type="button" @click="$emit('cancel')" style="float: right;">Cancel</button>
    
    <h1>Trek Registration</h1>
    <form @submit.prevent="registerTrek">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" v-model="form.name" required>
        </div>
        <div>
            <label for="location">Location:</label>
            <input type="text" id="location" name="location" v-model="form.location" required>
        </div>
        <div>
            <label for="difficulty">Difficulty:</label>
            <input type="text" id="difficulty" name="difficulty" v-model="form.difficulty" required>
        </div>
        <div>
            
            <label for="duration">Duration:</label>
            <input type="text" id="duration" name="duration" v-model="form.duration" required>
        </div>
        
        <div>
            <label for="available_slots">Available Slots:</label>
            <input type="number" id="available_slots" name="available_slots" v-model="form.available_slots" required>       
        </div>
        <div>
            <label for="staff_id">Staff ID:</label>
            <input type="text" id="staff_id" name="staff_id" v-model="form.staff_id" required>
        </div>
        <div>
            <label for="price">Price:</label>
            <input type="text" id="price" name="price" v-model="form.price" required>
        </div>
        <div>
            <label for="start_date">Start Date:</label>
            <input type="date" id="start_date" name="start_date" v-model="form.start_date" >
        </div>
        <div>
            <label for="end_date">End Date:</label>
            <input type="date" id="end_date" name="end_date" v-model="form.end_date" >  
        </div>
        
        

        <button type="submit">Register</button>
    </form>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'TrekRegister',
  emits: ['registered', 'cancel'],
  data() {
    return {
        form: {
            name: '',
            location: '',
            difficulty: '',
            duration: '',
            description: '',
            available_slots: '',
            staff_id: '',
            price: '',
            start_date: '',
            end_date: ''
        }

    };
  },
  methods: {
    async registerTrek() {
  try {
    const token = localStorage.getItem('admin_token'); 

    const response = await axios.post('http://localhost:5000/api/create_trek', this.form, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    this.$emit('registered'); 
    console.log('Trek registered successfully:', response.data);
    
    // 3. (Optional) Adjust your routing. Usually you just want to hide the form.
    this.$router.push('/admin'); 
  } catch (error) {
    console.error('Error registering trek:', error);
  }
}
  }
};

</script>