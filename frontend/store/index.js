export const state = () => {
  return {
    token: null,
    snack: null,
  };
};

export const mutations = {
  setToken(state, token) {
    state.token = token;
  },
  setSnack(state, snack) {
    state.snack = snack;
  },
};

export const actions = {
  async unsetAuthentication({ commit }) {
    await this.$cookies.remove('token');
    commit('setToken', null);
  },
  async setAuthentication({ commit }, token) {
    await this.$cookies.set('token', token);
    commit('setToken', token);
  },
  async getAuthentication({ commit }) {
    const token = this.$cookies.get('token');
    await this.$cookies.set('token', token);
    commit('setToken', token);
  },
};
