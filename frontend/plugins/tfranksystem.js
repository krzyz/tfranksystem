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

    async authorizedCallToAPI(route, method, body = undefined) {
      const token = this.$store.state.token;

      const headers = new Headers({
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      });

      return await this.fetchFromAPI(route, method, body, {
        headers,
      });
    },

    async postToAPI(route, body) {
      return await this.authorizedCallToAPI(route, 'POST', body);
    },

    async deleteFromAPI(route) {
      return await this.authorizedCallToAPI(route, 'DELETE');
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

    async getRanksHistory() {
      const response = await this.fetchFromAPI('historical');
      const ret = await response.json();
      return ret;
    },

    async createPlayer(body) {
      let res = await this.postToAPI('players', JSON.stringify(body));
      this.handleResponse(res, 'Player created successfully');
    },

    async createMatch(body) {
      let res = await this.postToAPI('matches', JSON.stringify(body));
      this.handleResponse(res, 'Match created successfully');
    },

    async deleteMatch(match_id) {
      let res = await this.deleteFromAPI(`matches/${match_id}`);
      this.handleResponse(res, 'Match removed successfully');
    },

    async authenticate(username, password) {
      const body = { username, password };
      const response = await this.fetchFromAPI(
        'oauth/token',
        'POST',
        JSON.stringify(body),
      );

      if (response.status != 200) {
        let reason = 'Unknown reason';
        const resJson = await response.json();
        if (resJson && resJson.message) {
          reason = resJson.message;
        }
        throw reason;
      }

      const ret = await response.json();
      return ret.token;
    },
  },
});
