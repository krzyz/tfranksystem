<template>
  <v-snackbar v-model="show" top :color="color">
    {{ message }}
    <v-spacer />
    <v-btn text @click.native="show = false">Close</v-btn>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      message: '',
      color: 'success',
    };
  },
  created: function() {
    this.$store.watch(
      state => state.snackbar.snack,
      () => {
        const snack = this.$store.state.snackbar.snack;
        if (snack !== null) {
          this.show = true;
          this.message = snack.message;
          this.color = snack.color;
          this.$store.commit('snackbar/setSnack', null);
        }
      },
    );
  },
};
</script>
