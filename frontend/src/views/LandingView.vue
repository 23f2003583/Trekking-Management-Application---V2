<template>
  <div class="landing-page"> 
    <h1>Welcome to the App</h1>
    
    <button @click="$router.push('/admin')">
      Admin View
    </button>

    <button @click="$router.push('/staff')">
      Staff View
    </button>
    
    <button @click="$router.push('/user')">
      User View
    </button>
  </div>
</template>

<script>

</script>
