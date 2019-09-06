<template>
  <v-card height="150">
    <v-footer 
      absolute
      class="font-weight-medium"
    >
      <div
        class="bg-custom text-center"
        cols="12"
      >
        mcerdeira — {{ new Date().getFullYear() }}
      </div>
    </v-footer>
  </v-card>
</template>
 
 <script>
 export default {
 
 }
 </script>
 
 <style>
    .bg-custom {
        background-color: dimgray;
        color: aliceblue;
    }
 </style>