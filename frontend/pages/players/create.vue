<template>
  <v-layout>
    <v-overlay :value="loading">
      <v-progress-circular
        :size="100"
        color="white"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
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
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-layout>
</template>

<script>
import { validationMixin } from 'vuelidate';
import { required, minLength } from 'vuelidate/lib/validators';

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
    loading: false,
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
    async submit() {
      this.$v.$touch();

      if (this.$v.$invalid) {
        this.showMessage({
          message: 'Invalid input!',
          color: 'warning',
        });
      } else {
        this.loading = true;
        await this.createPlayer({
          name: this.name,
          password: this.password,
        });
        this.loading = false;
      }
    },
  },
};
</script>
