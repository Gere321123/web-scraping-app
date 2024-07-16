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
        <input type="number" id="numberOfPeople" v-model.number="numberOfPeople" min="1" @change="updateAgesArray" />
      </div>

      <div class="form-group" v-for="(age, index) in ages" :key="index">
        <label :for="'age' + index">Életkor {{ index + 1 }}:</label>
        <input type="number" :id="'age' + index" v-model.number="ages[index]" min="0" />
      </div>

      <button type="submit">Keresés</button>
    </form>

    <div v-if="data.length" class="data-display">
      <div v-for="item in sortedData()" :key="item.title">
        <h2>{{ item.title }}</h2>
        <p>Ár: {{ item.price }}</p>
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
      numberOfPeople: 1,
      ages: [0],
      today: new Date().toISOString().split('T')[0],
      selectedSport: '',
      sportVisible: false,
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
        if (new Date(this.arrivalDate) > new Date(this.departureDate)) {
          alert('Érkezés dátuma nem lehet később mint a távozás dátuma!');
          return;
        }

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
          const responseData = await response.json();
          this.data = Object.entries(responseData).map(([key, value]) => ({
            title: key.replace('_price', '').replace(/^./, str => str.toUpperCase()),
            price: value
          }));
        } else {
          throw new TypeError('Expected JSON response from server');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    sortedData() {
      return this.data.sort((a, b) => {
        // Remove non-numeric characters and convert to a number for proper sorting
        const aPrice = parseFloat(a.price.replace(/[^\d,]/g, '').replace(',', '.'));
        const bPrice = parseFloat(b.price.replace(/[^\d,]/g, '').replace(',', '.'));
        return aPrice - bPrice;
      });
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
