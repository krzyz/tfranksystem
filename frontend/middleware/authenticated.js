export default function({ store, redirect }) {
  if (!store.state.token) {
    store.commit('snackbar/setSnack', {
      message: 'Must be logged in to access this page!',
      color: 'error',
    });

    return redirect('/');
  }
}
