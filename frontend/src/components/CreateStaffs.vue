<template>
  <div class="staff-register">
            <button type="button" @click="$emit('cancel')" style="float: right;">Cancel</button>
    
    <h1>Staff Registration</h1>
    <form @submit.prevent="registerStaff">
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
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="form.password" required>
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
        

        <button type="submit">Register</button>
    </form>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'StaffRegister',
  emits: ['registered', 'cancel'],
  data() {
    return {
        form: {
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

  async registerStaff() {
  try {
    const token = localStorage.getItem('admin_token'); 

    const response = await axios.post('http://localhost:5000/api/create_staff', this.form, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    this.$emit('registered'); 
    console.log('Staff registered successfully:', response.data);
    
  } catch (error) {
    console.error('Error registering staff:', error);
  }
}
  }
};

</script>