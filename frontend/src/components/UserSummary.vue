<template>
  <div>
    <h2>My Trek Booking Summary</h2>
    <p>Total Bookings: {{ summary.total }}</p>
    <p>Active: {{ summary.active_bookings }}</p>
    <p>Completed: {{ summary.completed_bookings }}</p>
    <p>Total Spent: ₹{{ summary.total_spent }}</p>
    
    <div v-if="summary.trek_names && summary.trek_names.length > 0">
      <h3>Trek-wise Bookings</h3>
      <Bar :data="countChartData" :options="{responsive: true}" />
    </div>
    
    <div style="margin-top: 20px;">
      <button @click="triggerExport">Export Booking History</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'UserSummary',
  components: { Bar },
  data() {
    return {
      summary: {},
      exmsg: null,
    }
  },
  computed: {
    countChartData() {
      return {
        labels: this.summary.trek_names || [],
        datasets: [
          {
            label: 'Bookings',
            data: this.summary.trek_counts || [],
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
          }
        ]
      }
    }
  },
  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://localhost:5000/api/user/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user_token')}`
          }
        })
        this.summary = response.data
        console.log(this.summary)
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    },
    async triggerExport() {
      try {
        const token = localStorage.getItem('user_token')
        const response = await axios.get('http://localhost:5000/api/export/bookings', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.exmsg = response.data
        alert("Export successful! Check your mail.")
      } catch (error) {
        console.error('Error exporting data:', error)
        alert("Failed to export data.")
      }
    }
  },
  mounted() {
    this.fetchSummary()
  }
}
</script>