<template>
  <v-layout>
    <v-flex class="text-center">
      Home
    </v-flex>
  </v-layout>
</template>

<script>
  export default {
    props: {
    },
    data: () => ({
    }),
    created () {
      this.$vuetify.theme.dark = true
    },
  }
</script>