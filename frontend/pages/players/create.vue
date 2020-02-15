<template>
  <v-layout>
    <form>
      <v-text-field
        v-model="name"
        :error-messages="nameErrors"
        label="Player name"
        required
        @input="$v.name.$touch()"
        @blur="$v.name.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="password"
        :error-messages="passwordErrors"
        type="password"
        label="User password"
        required
        @input="$v.password.$touch()"
        @blur="$v.password.$touch()"
      ></v-text-field>

      <v-btn class="mr-4" @click="submit">submit</v-btn>
    </form>
  </v-layout>
</template>

<script>
import { validationMixin } from 'vuelidate';
import { required, minLength } from 'vuelidate/lib/validators';
import { createPlayer } from '../../services/tfranksystem';

export default {
  middleware: 'authenticated',
  name: 'CreatePlayerComponent',
  mixins: [validationMixin],

  validations: {
    name: { required, minLength: minLength(3) },
    password: { required, minLength: minLength(6) },
  },
  data: () => ({
    name: '',
    password: '',
  }),
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.name.$dirty) return errors;
      !this.$v.name.minLength &&
        errors.push('Player name must be at least 3 characters long');
      !this.$v.name.required &&
        errors.push('Player name is required.');
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push('Password must be at least 6 characters long');
      !this.$v.password.required &&
        errors.push('Password is required.');
      return errors;
    },
  },
  methods: {
    submit() {
      createPlayer({ name: this.name, password: this.password });
    },
  },
};
</script>
