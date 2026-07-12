<template>
  <div class="staff-update">
            <button type="button" @click="$emit('cancel')" style="float: right;">Cancel</button>
    
    <h1>Staff Update</h1>
    <form @submit.prevent="updateStaff">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" v-model="form.name" required>
        </div>
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" v-model="form.username" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" v-model="form.email" required>
        </div>
        
        <div>
            <label>Assigned Treks:</label>
            <div class="checkbox-group" style="max-height: 150px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
                
                <div v-for="trek in availableTreks" :key="trek.id">
                    <input 
                        type="checkbox" 
                        :id="'trek_' + trek.id" 
                        :value="trek.id" 
                        v-model="form.treks"
                    >
                    <label :for="'trek_' + trek.id">{{ trek.name }}</label>
                </div>
                
            </div>
        </div>

        <button type="submit">Update</button>
    </form>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'StaffUpdate',
  emits: ['updated', 'cancel'],

  props: {
    staff: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
        form: {
            id:'',
            name: '',
            username: '',
            email: '',
            password: '',
            treks: []
        },
        availableTreks: []

    };
  },

  mounted() {
    this.fetchAvailableTreks();

    if (this.staff) {
      this.form.id = this.staff.id;
      this.form.name = this.staff.name;
      this.form.username = this.staff.username;
      this.form.email = this.staff.email;
      if (this.staff.treks && Array.isArray(this.staff.treks)) {
            this.form.treks = this.staff.treks.map(trek => trek.id);
        } else {
            this.form.treks = []; 
        }
    }
  },
  methods: {
    async fetchAvailableTreks() {
      try {
        const token = localStorage.getItem('admin_token'); 
        const response = await axios.get('http://localhost:5000/api/get_treks', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.availableTreks = response.data;
      } catch (error) {
        console.error('Error fetching treks:', error);
      }
    },
    async updateStaff() {
  try {
    const token = localStorage.getItem('admin_token'); 

    const response = await axios.put(`http://localhost:5000/api/update_staff/${this.staff.id}`, this.form, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    this.$emit('updated'); 
    console.log('Staff updated successfully:', response.data);
    
  } catch (error) {
    console.error('Error updating staff:', error);
  }
}
  }
};

</script>