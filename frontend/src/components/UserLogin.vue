<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
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
    <a href="#" @click.prevent="$emit('show-register')">Don't have an account? Register here.</a>
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
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/api/login', this.form);
        
        console.log('Login successful:', response.data);
        
        const token = response.data.data.access_token;
        localStorage.setItem('token', token); 
        
        this.$emit('login-successful'); 
        this.$router.push('/user'); 
        
      } catch (error) {
        console.error('Error logging in:', error);
        alert('Invalid username or password'); 
      }
    }
  }
}
</script>