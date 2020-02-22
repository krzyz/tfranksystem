<template>
  <v-app dark>
    <v-overlay :value="loading">
      <v-progress-circular :size="100" color="white" indeterminate />
    </v-overlay>
    <v-navigation-drawer v-model="drawer" app clipped>
      <v-list dense>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app dense clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>Towerfall rank system</v-toolbar-title>
      <v-spacer />
      <v-dialog
        v-if="!authorized"
        v-model="loginModal"
        max-width="290"
      >
        <template v-slot:activator="{ on }">
          <v-btn text small v-on="on">Login</v-btn>
        </template>
        <v-card>
          <form>
            <v-card-title class="headline">Login</v-card-title>
            <v-card-text>
              <v-text-field
                v-model="username"
                label="Player name"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                type="password"
                label="User password"
                required
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="submit">Log in</v-btn>
            </v-card-actions>
          </form>
        </v-card>
      </v-dialog>
      <span v-if="authorized">
        <v-btn text @click="logout">Log out</v-btn>
      </span>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer app>
      <span>&copy; 2020</span>
    </v-footer>
    <mainSnackbar />
  </v-app>
</template>

<script>
import mainSnackbar from '../components/mainSnackbar';

export default {
  components: {
    mainSnackbar,
  },
  data() {
    return {
      username: null,
      password: null,
      loginModal: false,
      drawer: null,
      loading: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Dashboard',
          to: '/',
        },
        {
          icon: 'mdi-account-multiple',
          title: 'Player list',
          to: '/players',
        },
        {
          icon: 'mdi-account-plus',
          title: 'Add player',
          to: '/players/create',
        },
        {
          icon: 'mdi-history',
          title: 'Matches list',
          to: '/matches',
        },
        {
          icon: 'mdi-plus-circle',
          title: 'Add match',
          to: '/matches/create',
        },
      ],
      title: 'Towerfall Rank System',
    };
  },
  computed: {
    authorized() {
      if (this.$store.state.token) {
        return true;
      }
      return false;
    },
  },
  async created() {
    this.$store.dispatch('getAuthentication');
  },
  methods: {
    async submit() {
      this.loginModal = false;
      this.loading = true;
      try {
        const token = await this.authenticate(
          this.username,
          this.password,
        );

        this.$store.dispatch('setAuthentication', token);

        this.showMessage({
          message: 'Sucessfully logged in',
          color: 'success',
        });
      } catch (error) {
        this.showMessage({
          message: `Error: ${error}`,
          color: 'error',
        });
      } finally {
        this.loading = false;
      }
    },
    async logout() {
      this.loading = true;
      this.$store.dispatch('unsetAuthentication');
      this.showMessage({
        message: 'Sucessfully logged out',
        color: 'success',
      });
      this.loading = false;
      this.$router.push('/');
    },
  },
};
</script>
