<template>
<div>
    <div v-if="!isLoggedIn">    
        <UserLogin v-if="!showRegister" @login-successful="handlelogin" @show-register="showRegister = true" />
        <UserRegister v-else @registered="handleRegisteration" @show-login="showRegister = false" />
    </div>

    <div v-else>
        <UserDashboard />
    </div>

</div>
</template>



<script>
import UserDashboard from '@/components/UserDashboard.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';

export default {
    name: 'UserView',
    components: {
        UserRegister,
        UserLogin,
        UserDashboard
    },
    data() {
        return {
            isLoggedIn: false,
            showRegister: false
        };
    },
    methods: {
        handlelogin() {
            this.isLoggedIn = true;
        },
        handleRegisteration() {
            this.showRegister = false;
            this.isLoggedIn = true;
        }
    }
};


</script>