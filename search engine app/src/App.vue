<template>
  <div id="app">
    <img title="Strudel means 'whirlpool' in German" alt="Vue logo" src="./assets/logo.png">
    <p>v0.1.6</p>
    <SearchBar/>    
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'

export default {
  name: 'app',
  mounted(){
    let url = process.env.VUE_APP_WARM_API;    
    fetch(url)
      .then(
          function(response) {
              console.log(response.status);
              if (response.status !== 200) {
                  console.log(response.json);
                  return;
              } else {
                  response.json().then(function(d) {
                      console.log(d);
                  }.bind(this));
              }
          }.bind(this)
      );
  },

  components: {
    SearchBar
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
