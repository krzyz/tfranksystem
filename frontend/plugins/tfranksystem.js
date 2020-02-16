import Vue from 'vue';

Vue.mixin({
  methods: {
    async handleResponse(res, message) {
      if (res.ok) {
        this.showMessage({
          message,
          color: 'success',
        });
      } else {
        let reason = res.statusText;
        const resJson = await res.json();
        if (resJson && resJson.message) {
          reason = resJson.message;
        }

        this.showMessage({
          message: `Error: ${reason}`,
          color: 'error',
        });
      }
    },

    async postToAPI(route, body) {
      const token = this.$store.state.token;

      const headers = new Headers({
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      });

      return await this.fetchFromAPI(route, 'POST', body, {
        headers,
      });
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
      let res = await this.postToAPI('players', JSON.stringify(body));
      this.handleResponse(res, 'Player created successfully');
    },

    async createMatch(body) {
      let res = await this.postToAPI('matches', JSON.stringify(body));
      this.handleResponse(res, 'Match created successfully');
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
