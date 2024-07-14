<template>
    <div>
      <h1>Adatok</h1>
      <div v-if="data.length">
        <div v-for="item in data" :key="item.title">
          <h2>{{ item.title }}</h2>
          <p>{{ item.price }}</p>
        </div>
      </div>
      <div v-else>
        <p>Nincs adat.</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        data: []
      };
    },
    async created() {
      try {
        const response = await fetch('/api/data');
        this.data = await response.json();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
  };
  </script>
  
  <style>
  /* Tetszés szerinti stílusok */
  </style>
  