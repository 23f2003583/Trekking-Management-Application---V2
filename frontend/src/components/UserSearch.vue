<template>
  <div>
    <h2>Search Treks</h2>
    
    <div>
      <input
        type="text"
        v-model="searchQuery"
        @keyup.enter="performSearch"
        placeholder="Search for treks by name..."
      />
      <button @click="performSearch">Search</button>
    </div>

    <div v-if="hasSearched">
      <h3>Search Results ({{ results.length }})</h3>
      
      <div v-if="results.length > 0">
        <ul>
          <li v-for="trek in results" :key="trek.id">
            <p>Trek ID: {{ trek.id }}</p>
            <p>Name: {{ trek.name }}</p>
            <p>Location: {{ trek.location }}</p>
            <p>Start Date: {{ trek.start_date }}</p>
            <p>End Date: {{ trek.end_date }}</p>
            <p>Status: {{ trek.status }}</p>
            <hr />
          </li>
        </ul>
      </div>
      
      <p v-else>No treks found matching "{{ lastSearched }}".</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserSearch',
  data() {
    return {
      searchQuery: '',
      lastSearched: '',
      hasSearched: false,
      results: []
    };
  },
  methods: {
    async performSearch() {
      if (!this.searchQuery.trim()) {
        alert("Please enter a trek name to search.");
        return;
      }

      try {
        // Remember to use user_token for the trekker's side!
        const token = localStorage.getItem('user_token');
        
        const response = await axios.get('http://localhost:5000/api/user/search_treks', {
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