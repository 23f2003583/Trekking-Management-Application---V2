<template>
  <div class="trek-update">
    <button type="button" @click="$emit('cancel')" style="float: right;">Cancel</button>
    
    <h1>Trek Update</h1>
    <form @submit.prevent="updateTrek">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" v-model="form.name"  required>
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
        
        

        <button type="submit">Update Trek</button>
    </form>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'TrekUpdate',
  emits: ['updated', 'cancel'],

    props :{
        trek:{
            type: Object,
            required: true
        }
    },

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

  mounted() {
    if (this.trek) {
      this.form.id = this.trek.id;
      this.form.name = this.trek.name;
      this.form.location = this.trek.location;
      this.form.difficulty = this.trek.difficulty;
      this.form.duration = this.trek.duration;
      this.form.description = this.trek.description;
      this.form.available_slots = this.trek.available_slots;
      this.form.staff_id = this.trek.staff_id;
      this.form.price = this.trek.price;
      if (this.trek.start_date) {
        this.form.start_date = this.trek.start_date.split('T')[0];
      }
        
      if (this.trek.end_date) {
        this.form.end_date = this.trek.end_date.split('T')[0];
      }
      
    }
  },
  methods: {
    async updateTrek() {
  try {
const token = localStorage.getItem('admin_token') || localStorage.getItem('staff_token');
    const response = await axios.put(`http://localhost:5000/api/update_trek/${this.form.id}`, this.form, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    this.$emit('updated'); 

    console.log('Trek updated successfully:', response.data);
    this.$emit('trekUpdated');
    
  } catch (error) {
    console.error('Error updating trek:', error);
  }
}
  }
};

</script>