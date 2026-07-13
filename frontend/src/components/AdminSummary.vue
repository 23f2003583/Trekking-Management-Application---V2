<template>
  <div>
    <h2>Admin Dashboard Summary</h2>
    <div v-if="summary">
      <p>Total Platform Bookings: {{ summary.total_bookings }}</p>
      <p>Total Platform Revenue: ₹{{ summary.total_revenue }}</p>
      
      <!-- Added a flex container so the charts sit side-by-side -->
      <div style="display: flex; gap: 40px; flex-wrap: wrap; margin-top: 30px;">
        
        <!-- Original Bookings Chart -->
        <div v-if="summary.trek_names && summary.trek_names.length > 0" style="flex: 1; min-width: 300px;">
          <h3>Bookings per Trek</h3>
          <Bar :data="countChartData" :options="{ responsive: true }" />
        </div>

        <!-- NEW: Staff Assigned Treks Chart -->
        <div v-if="summary.staff_names && summary.staff_names.length > 0" style="flex: 1; min-width: 300px;">
          <h3>Assigned Treks per Staff</h3>
          <Bar :data="staffChartData" :options="{ responsive: true }" />
        </div>

      </div>
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
  name: 'AdminSummary',
  components: { Bar },
  data() {
    return {
      summary: {},
    }
  },
  computed: {
    // Existing Chart Data
    countChartData() {
      return {
        labels: this.summary.trek_names || [],
        datasets: [
          {
            label: 'Total Bookings',
            data: this.summary.trek_counts || [],
            backgroundColor: 'rgba(153, 102, 255, 0.5)',
          },
        ],
      }
    },
    // NEW: Staff Chart Data
    staffChartData() {
      return {
        labels: this.summary.staff_names || [],
        datasets: [
          {
            label: 'Assigned Treks',
            data: this.summary.staff_trek_counts || [],
            backgroundColor: 'rgba(54, 162, 235, 0.5)', // Blue color to distinguish it
          },
        ],
      }
    }
  },
  methods: {
    async fetchSummary() {
      try {
        const token = localStorage.getItem('admin_token')
        const response = await axios.get('http://localhost:5000/api/admin/summary', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.summary = response.data
        console.log(this.summary)
      } catch (error) {
        console.error('Error fetching admin summary:', error)
      }
    },
  },
  mounted() {
    this.fetchSummary()
  },
}
</script>