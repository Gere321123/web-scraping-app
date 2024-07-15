<template>
  <div class="container">
    <h1>Utazás biztositás kereső</h1>
    <form @submit.prevent="fetchData">
      <div class="form-group">
        <label for="arrival">Érkezés dátuma:</label>
        <input type="date" id="arrival" v-model="arrivalDate" :min="today" required />
      </div>

      <div class="form-group">
        <label for="departure">Távozás dátuma:</label>
        <input type="date" id="departure" v-model="departureDate" :min="today" required />
      </div>

      <div class="form-group">
        <label for="numberOfPeople">Foglalók száma:</label>
        <input type="number" id="numberOfPeople" v-model.number="numberOfPeople" min="1" @change="updateAgesArray" required />
      </div>

      <div class="form-group" v-for="(age, index) in ages" :key="index">
        <label :for="'age' + index">Életkor {{ index + 1 }}:</label>
        <input type="number" :id="'age' + index" v-model.number="ages[index]" min="0" required />
      </div>

      <DDOR_Travel_Type 
      :selectedSport="selectedSport" 
      @update:selectedSport="updateSelectedSport"
    />

      <button type="submit">Keresés</button>
    </form>

    <div v-if="data" class="data-display">
      <div>
        <h2>DDOR{{ data.title }}</h2>
        <p>Ár: {{ data.price }}</p>
      </div>
    </div>
    <div v-else>
      <p>Nincs adat.</p>
    </div>
  </div>
</template>

<script>
import DDOR_Travel_Type from './DDOR_Travel_Type.vue';
export default {
  components: {
    DDOR_Travel_Type
  },
  data() {
    return {
      data: null,
      arrivalDate: '',
      departureDate: '',
      numberOfPeople: 1,
      ages: [0],
      today: new Date().toISOString().split('T')[0],
      selectedSport: '',
    };
  },
  methods: {
    updateSelectedSport(sport) {
      this.selectedSport = sport;
    },
    updateAgesArray() {
      const newAgesArray = [];
      for (let i = 0; i < this.numberOfPeople; i++) {
        newAgesArray.push(this.ages[i] !== undefined ? this.ages[i] : 0);
      }
      this.ages = newAgesArray;
    },
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
            ages: this.ages,
            sport: this.selectedSport,
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
.container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}
label {
  margin-bottom: 5px;
}
input {
  margin-top: 5px;
  padding: 5px;
  width: 100%;
  box-sizing: border-box;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
}
.data-display {
  margin-top: 20px;
}
</style>
