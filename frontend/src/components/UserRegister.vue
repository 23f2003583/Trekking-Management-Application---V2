<template>
  <div class="user-register">
    <button style="float: right; color:red" @click="cancel()">
          cancel
      </button>
    <h1>User Registration</h1>
    <form @submit.prevent="registerUser">
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
        <button type="submit">Register</button>
    </form>

    <a href="#" @click.prevent="$emit('show-login')">Already have an account? Login here.</a>

  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'UserRegister',
  emits: ['registered', 'show-login'],
  data() {
    return {
        form: {
            username: '',
            email: '',
            password: '',
            name: ''
        }

    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post('http://localhost:5000/api/register', this.form);
        this.$emit('registered'); 
        localStorage.setItem('user_token', response.data.access_token);
        console.log('User registered successfully:', response.data);
        this.$router.push('/'); 

      } catch (error) {
        alert(error.response.data.message);
        console.error('Error registering user:', error);
      }
    },
        cancel() {
            this.$router.push('/');
        }
  }
};

</script>