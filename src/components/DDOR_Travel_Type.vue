<template>
    <div class="container">
        
      <input type="text" v-model="searchQuery" placeholder="Keresés..." class="search-bar" />
      <ul class="border">
        <li 
          v-for="sport in filteredSports" 
          :key="sport" 
          :class="{'text': true, 'selected': selectedSport === sport}" 
          @click="selectSport(sport)"
        >
          {{ sport }}
        </li>
      </ul>
      <div v-if="selectedSport !== null">
        <p>Kiválasztott sport: {{ selectedSport }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
    selectedSport: {
      type: String,
      default: ''
    }
  },
    computed: {
    filteredSports() {
      return this.sports.filter(sport => 
        sport && sport.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    selectSport(sport) {
        this.$emit('update:selectedSport', sport);
    }
  },
    data() {
      return {
      searchQuery: '',
        sports: [
          "Aerobik",
          "Aeroklubovi",
          "Aikido",
          "Atletika - laka",
          "Atletika - teška, izuzev rvanja i boksa",
          "Badminton",
          "Biciklizam - planinski biciklizam (mountain bike)",
          "Biciklizam - sa trkama svih vrsta i treninzima za njih",
          "Bilijar",
          "Bodibilding",
          "Boks i kik-boks",
          "Dizanje tegova",
          "Džet ski",
          "Džez balet",
          "Džijudžica, džudo i sambo",
          "Fudbal",
          "Gimnastika - proste vežbe",
          "Gimnastika - vežbe na spravama",
          "Go Kart",
          "Golf",
          "Hokej - na ledu",
          "Hokej - na rolšuama",
          "Hokej - na travi",
          "Jahanje - galopske i kasačke trke",
          "Jahanje - sportsko jahanje",
          "Jahanje - trke preko prepona",
          "Jedrenje, veslanje i skijanje na vodi - na moru",
          "Jedrenje, veslanje i skijanje na vodi - na unutrašnjim vodama",
          "Joga",
          "Kajak - vožnja",
          "Kapuera",
          "Karate",
          "Kendo",
          "Kjokošin kai karate",
          "Klizanje na ledu",
          "Košarka, basket",
          "Kuglanje",
          "Logorovanje sa upražnjavanjem raznih sportskih disciplina",
          "Lovački sport",
          "Mačevanje",
          "Motociklizam, automobilizam i mopedizam - kontrolori i pratioci u automobilu ili na motociklu i automoto trkama",
          "Motociklizam, automobilizam i mopedizam - mopedizam - takmičenje i treninzi",
          "Odbojka",
          "Organizatori sportskih takmičenja - za auto-moto sport (starteri, merači vremena, kontrolori staze, zapisničari i redari)",
          "Organizatori sportskih takmičenja - za ostale sportove",
          "Planinarenje - hodanje planinskim putevima do 3 000 metara nadmorske visine, isključujući penjanje po vrletima i penjanje na glečere bez obzira na visinu",
          "Ples - akrobatski",
          "Ples - klasični",
          "Plivanje",
          "Plivanje - maratonsko plivanje",
          "Plivanje - na bazenima",
          "Plivanje - na moru",
          "Plivanje - na unutrašnjim vodama",
          "Ragbi",
          "Ribarenje - na otvorenom moru",
          "Ribarenje - podvodni ribolov",
          "Ribarenje - priobalna, jezerska i na rekama",
          "Rolanje - rolerima, rolšuama",
          "Rukomet",
          "Rvanje - grčko-rimski stil",
          "Rvanje - slobodni stil",
          "Sankanje - na bobu",
          "Sankanje - na običnim sankama",
          "Sankanje - na sportskim sankama za takmičenje",
          "Skijanje - rekreativno",
          "Skijanje - trening i učešće osiguranika u takmičenjima profesionalnih ili amaterskih sportista registrovanog člana sportske organizacije",
          "Skokovi u vodu",
          "Speleolozi",
          "Sportske sudije",
          "Stoni tenis",
          "Streljački sport",
          "Tekvondo",
          "Tenis",
          "Tociljanje",
          "Treneri - ostali aktivni sportski radnici (vođa puta, fizioterapeut, lekar i druga lica)",
          "Treneri - za sportove od 1 do 4 razreda opasnosti",
          "Treneri - za sportove od 5 do 7 razreda opasnosti",
          "Treneri - za sportove od 8 do 9 razreda opasnosti",
          "Triatlon",
          "Trke motornih sportskih čamaca",
          "Učenici auto-škola",
          "Učenici fiskulture",
          "Vaterpolo",
          "Vazduhoplovno modelarstvo - bez rizika letenja",
          "Vežbe - fitness",
          "Vežbe - gimnastika na spravama",
          "Vežbe - sletovi",
          "Šah"
        ]
      };
    }
  };
  </script>
  
  <style scoped>
  .container {
    width: 300px;
    margin: 0 auto;
  }
  
  .search-bar {
    width: 100%;
    padding: 8px;
  }
  
  .border {
    list-style: none;
    padding: 0;
    border: 1px solid #ccc;
    max-height: 200px; /* Maximális magasság a lista tartalmának korlátozásához */
    overflow-y: auto; /* Görgetősáv megjelenítése, ha szükséges */
  }
  
  .text {
    padding: 8px;
    cursor: pointer;
  }
  
  .selected {
    background-color: #f0f0f0;
  }
  
  /* Szép scrollbar stílus */
  .border::-webkit-scrollbar {
    width: 8px;
  }
  
  .border::-webkit-scrollbar-track {
    background: #f1f1f1;
  }
  
  .border::-webkit-scrollbar-thumb {
    background-color: #888;
    border-radius: 4px;
  }
  
  .border::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
  </style>
  
  