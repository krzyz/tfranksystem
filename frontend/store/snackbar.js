export const state = () => {
  return {
    snack: null,
  };
};

export const mutations = {
  setSnack(state, snack) {
    state.snack = snack;
  },
};
