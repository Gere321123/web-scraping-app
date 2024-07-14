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
    const response = await fetch('http://localhost:5000/api');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      this.data = await response.json();
    } else {
      throw new TypeError('Expected JSON response from server');
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}



  };
  </script>
  
  <style>
  /* Tetszés szerinti stílusok */
  </style>
  