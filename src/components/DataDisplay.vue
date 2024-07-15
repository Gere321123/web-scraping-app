<template>
  <div>
    <h1>Adatok</h1>
    <form @submit.prevent="fetchData">
      <label for="arrival">Érkezés dátuma:</label>
      <input type="date" id="arrival" v-model="arrivalDate" required />
      
      <label for="departure">Távozás dátuma:</label>
      <input type="date" id="departure" v-model="departureDate" required />
      
      <label for="age">Életkor:</label>
      <input type="number" id="age" v-model="age" required />

      <button type="submit">Keresés</button>
    </form>

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
      data: [],
      arrivalDate: '',
      departureDate: '',
      age: ''
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://localhost:5000/api', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            arrivalDate: this.arrivalDate,
            departureDate: this.departureDate,
            age: this.age
          })
        });
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
  }
};
</script>

<style>
/* Tetszés szerinti stílusok */
form {
  margin-bottom: 20px;
}
label {
  display: block;
  margin-top: 10px;
}
input {
  display: block;
  margin-top: 5px;
}
button {
  margin-top: 10px;
}
</style>
