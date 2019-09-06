<template>
    <div class="container">
        <input placeholder="Search term" class="form-control input-sm" @keyup.enter="trigger_click" autofocus v-model="query" id="search_text" type="text">
        <br>
        <button class="btn btn-light" type="submit" @click="search_clicked" ref="button_search">Search</button>
        <br>      
        <br>       
        <div v-if="showResult && !processing && result.length == 0">
            Nothing to show, No results.
        </div>
        <h4 v-else-if="processing">
            Searching...
        </h4>  
        <h4 v-else-if="showResult && !processing">
            {{result[0].count}} results:
        </h4>
		
        <div v-for="(result, title) in getDataGrouped" :key="title" >  
            <details>
                <summary><strong>Movie: {{title}}</strong></summary>      
                <MovieExtra :movie="title" v-if="showResult && !processing"/>
                <div v-for="(v, index) in result" :key="v.tag" >                    
                    Song: {{index + 1}} {{v.song}} - Album: {{v.tag}}      
                    <br v-if="index==result.length-1">
                    <a v-if="index==result.length-1" :href="v.url" target="_blank">See Full Soundtrack</a>
                </div>                 
             </details>             
        </div>
        <CustomFooter v-if="showResult && !processing"/>     
    </div>         
</template>

<script>
import CustomFooter from './CustomFooter.vue'
import MovieExtra from './MovieExtra.vue'

export default {
  components: {
    CustomFooter, MovieExtra
  },

  mounted(){      
      this.showResult = false;
      this.processing = false;
  },

  computed:{
      getDataGrouped:function () {
            return _.groupBy(this.result, 'title') ;
    }
  },
  
  methods: {
    set_data: function(data){
        this.result = data;
    },

    trigger_click: function(){
        this.$refs.button_search.click();
    },

    search_clicked: function(event){      
      this.showResult = true;
      this.processing = true;
      this.result = []
      let query = this.query;
      let base_url = process.env.VUE_APP_ROOT_API;
      let url = `${base_url}/${query}`;
      console.log(url);
      fetch(url)
        .then(
            function(response) {
                console.log(response.status);
                if (response.status !== 200) {
                    this.processing = false;
                    console.log(response.json);
                    return;
                } else {
                    response.json().then(function(d) {
                        this.processing = false;
                        console.log(d);
                        this.result = d;
                    }.bind(this));
                }
            }.bind(this)
        );
    },
  },
  data: function() {
      return {             
        processing: false,
        showResult: false,
        query: "",
        result: []
      }
  },
}
</script>

<style>
details {
    padding: .5em .5em 0;
	background: rgb(196, 187, 187);
}

summary {
    margin: -.5em -.5em 0;
    padding: .5em;
}

details[open] {
    padding: .5em;
}

details[open] summary {
    border-bottom: 1px solid #aaa;
    margin-bottom: .5em;
}

</style>
