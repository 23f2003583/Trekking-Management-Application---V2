<template>
  <div class="user-register">
    <h1>User Registration</h1>
    <form @submit.prevent="registerUser">
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
        <button type="submit">Register</button>
    </form>

    <a href="#" @click.prevent="$emit('show-login')">Already have an account? Login here.</a>

  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'UserRegister',
  emits: ['register'],
  data() {
    return {
        form: {
            username: '',
            email: '',
            password: ''
        }

    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post('http://localhost:5000/api/register', this.form);
        this.$emit('registered'); 
        console.log('User registered successfully:', response.data);
      } catch (error) {
        console.error('Error registering user:', error);
      }
      this.$router.push('/user'); 
    }
  }
};

</script>