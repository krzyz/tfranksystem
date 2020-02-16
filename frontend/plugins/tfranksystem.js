import Vue from 'vue';

Vue.mixin({
  methods: {
    async postToAPI(route, body) {
      const token = this.$store.state.token;

      const headers = new Headers({
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      });

      this.fetchFromAPI(route, 'POST', body, { headers });
    },
    async fetchFromAPI(
      route,
      method = 'GET',
      body = null,
      additionalOptions = null,
    ) {
      const mode = 'cors';

      const options = {
        method,
        mode,
        ...(body ? { body } : {}),
        ...additionalOptions,
      };

      return await fetch(`${process.env.API_URL}/${route}`, options);
    },
    async getPlayers() {
      const response = await this.fetchFromAPI('players');
      const ret = await response.json();
      return ret.players;
    },
    async getMatches() {
      const response = await this.fetchFromAPI('matches');
      const ret = await response.json();
      return ret.matches;
    },
    async createPlayer(body) {
      return await this.postToAPI('players', JSON.stringify(body));
    },
    async createMatch(body) {
      return await this.postToAPI('matches', JSON.stringify(body));
    },
    async authenticate(username, password) {
      const body = { username, password };
      const response = await this.fetchFromAPI(
        'oauth/token',
        'POST',
        JSON.stringify(body),
      );

      if (response.status != 200) {
        return false;
      }

      const ret = await response.json();
      return ret.token;
    },
  },
});
