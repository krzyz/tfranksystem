import Vue from 'vue';

Vue.mixin({
  methods: {
    showMessage: function(snack) {
      this.$store.commit('snackbar/setSnack', snack);
    },
  },
});
