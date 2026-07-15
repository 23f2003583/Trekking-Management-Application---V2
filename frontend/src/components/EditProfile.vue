<template>
  <div class="profile">
    <h1>My Profile</h1>
    <form @submit.prevent="updateProfile">
        
      <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" v-model="form.name" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" v-model="form.email" required>
        </div>
        
      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfilePage',
  data() {
    return {
      form: {
        name: '',
        email: ''
      }
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('user_token') || localStorage.getItem('staff_token');
      const response = await axios.get('http://localhost:5000/api/profile', {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.form = response.data;
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem('user_token') || localStorage.getItem('staff_token');
        await axios.put('http://localhost:5000/api/profile', this.form, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile.');
      }
    }
  }
};
</script>