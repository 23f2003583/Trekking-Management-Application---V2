<template>
  <div>
    <button style="float: right; color:red" @click="cancel()">
          cancel
    </button>
    <h1>Admin Login</h1>
    <form @submit.prevent="handleAdminLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="form.username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="form.password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {  
        username: '',
        password: ''
      }
    };
  },
  methods: {
    async handleAdminLogin() {
      try {
        const response = await axios.post('http://localhost:5000/api/admin/login', this.form);
        
        console.log('Login successful:', response.data);
        
        const token = response.data.data.access_token;
        localStorage.setItem('admin_token', token); 
        
        this.$emit('logged-in'); 
        this.$router.push('/admin'); 
        
      } catch (error) {
        console.error('Error logging in:', error);
        alert('Invalid username or password'); 
      }
    },
        cancel() {
            this.$router.push('/');
        }
  }
}
</script>