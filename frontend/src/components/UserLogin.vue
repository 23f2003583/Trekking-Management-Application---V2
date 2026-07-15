<template>
  <div>
    <button style="float: right; color:red" @click="cancel()">
          cancel
    </button>
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
        localStorage.setItem('user_token', token);
        
        this.$emit('login-successful'); 
        this.$router.push('/user'); 
        
      } catch (error) {
            if (error.response && error.response.data && error.response.data.message) {
                
                alert(error.response.data.message); 
                console.error("Backend Error:", error.response.data.message);
                
            } else {
                alert("A network error occurred.");
                console.error("Axios Error:", error.message);
            }
        }
    },
        cancel() {
            this.$router.push('/');
        }
  }
}
</script>