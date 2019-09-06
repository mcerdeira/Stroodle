<template>
    <div>
        <img class="resize" :src="getImage" alt=""/>
        <br>
        <strong>Rated: {{rating}}</strong>
        <br>
        <em v-if="(plot != null)">{{plot}}</em>
        <br>
        <a v-if="(website != null)" :href="website" target="_blank">Movie Site</a>
    </div>
</template>

<script>
export default {
    computed: {
        getImage: function(){
            return !this.omdb_img ? this.default_img : this.omdb_img;
        }
    },
    mounted() {
        this.search(this.movie);
    },

    methods: {
        _movie2searchObj: function(movie){
            let regExp = /\(([^)]+)\)/;
            let title = movie;
            let matches = regExp.exec(title);
            let obj = {term: title.replace(matches[0].trim(), ""), year: matches[1]};
            return obj;
        },

        valid_url: function(url){
            let valid = /^(ftp|http|https):\/\/[^ "]+$/.test(url);
            if(valid){
                return url;
            } else {
                return null;
            }
        },

        search: function(movie){
            let base_url = process.env.VUE_APP_OMDB_API;
            let key = process.env.VUE_APP_OMDB_KEY;
            let {term, year} = this._movie2searchObj(movie); 

            let url = `${base_url}?apikey=${key}&t=${term}&y=${year}`;
            console.log(url);
            fetch(url)
                .then(
                    function(response) {
                        console.log(response.status);
                        if (response.status !== 200) {
                            console.log(response.json);
                            return;
                        } else {
                            response.json().then(function(d) {
                                if(d.Poster){
                                    this.omdb_img = d.Poster;
                                }
                                if(d.Rated){
                                    this.rating = d.Rated;
                                }
                                if(d.Plot){
                                    this.plot = d.Plot;
                                }
                                this.website = this.valid_url(d.Website);
                                console.log(d);
                            }.bind(this));
                        }
                    }.bind(this)
                );
        }
    },

    props: {
        movie: String,
    },

    data: function(){
        return {
            default_img: require("@/assets/no-poster.jpg"),
            omdb_img: null,
            rating: 'N/A',
            website: null,
            plot: null,
        }
    }
}
</script>

<style>
img.resize {
  max-width:20%;
  max-height:20%;
}
</style>