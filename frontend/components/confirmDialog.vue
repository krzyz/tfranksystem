<template>
  <v-dialog v-model="dialog" max-width="290">
    <v-card>
      <v-card-title class="headline">{{ text }}</v-card-title>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn color="base" text @click.stop="dialog = false">
          Cancel
        </v-btn>

        <v-btn color="red" text @click.stop="confirm()">
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialogComponent',
  props: {
    value: Boolean,
    text: {
      type: String,
      default: 'Are you sure?',
    },
  },
  computed: {
    dialog: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit('input', value);
      },
    },
  },
  methods: {
    confirm() {
      this.dialog = false;
      this.$emit('confirm');
    },
  },
};
</script>
