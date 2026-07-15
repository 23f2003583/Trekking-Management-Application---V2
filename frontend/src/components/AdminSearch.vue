<template>
  <div class="search-wrapper">
    <h2>Global Search</h2>
    
    <div >
      <input
        type="text"
        v-model="searchQuery"
        @keyup.enter="performSearch"   />
      <button 
        @click="performSearch"
      >
        Search
      </button>
    </div>

    <div v-if="hasSearched">
      
      <div class="result-card">
        <h3>Treks ({{ results.treks.length }})</h3>
        <ul v-if="results.treks.length > 0">
          <li v-for="trek in results.treks" :key="'t-'+trek.id">
            <strong>{{ trek.name }}</strong> - {{ trek.location }}
          </li>
        </ul>
        <p v-else class="empty-text">No treks found matching "{{ lastSearched }}".</p>
      </div>

      <div class="result-card">
        <h3>Staff Members ({{ results.staff.length }})</h3>
        <ul v-if="results.staff.length > 0">
          <li v-for="staff in results.staff" :key="'s-'+staff.id">
            <strong>{{ staff.name }}</strong> ({{ staff.email }})
          </li>
        </ul>
        <p v-else class="empty-text">No staff found matching "{{ lastSearched }}".</p>
      </div>

      <div class="result-card">
        <h3>Trekkers ({{ results.users.length }})</h3>
        <ul v-if="results.users.length > 0">
          <li v-for="user in results.users" :key="'u-'+user.id">
            <strong>{{ user.name }}</strong> ({{ user.email }})
          </li>
        </ul>
        <p v-else class="empty-text">No users found matching "{{ lastSearched }}".</p>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminSearch',
  data() {
    return {
      searchQuery: '',
      lastSearched: '',
      hasSearched: false,
      results: {
        treks: [],
        staff: [],
        users: []
      }
    };
  },
  methods: {
    async performSearch() {
      if (!this.searchQuery.trim()) {
        alert("Please enter a name to search.");
        return;
      }

      try {
        const token = localStorage.getItem('admin_token');
        
        const response = await axios.get('http://localhost:5000/api/admin/search', {
          headers: { Authorization: `Bearer ${token}` },
          params: { q: this.searchQuery } 
        });

        this.results = response.data;
        this.lastSearched = this.searchQuery;
        this.hasSearched = true;
        
      } catch (error) {
        console.error("Search failed:", error);
        alert("An error occurred while searching.");
      }
    }
  }
};
</script>
