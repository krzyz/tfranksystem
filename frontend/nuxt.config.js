require('dotenv').config();

import colors from 'vuetify/es5/util/colors';

export default {
  mode: 'spa',
  head: {
    titleTemplate: '%s - Towerfall Rank System',
    title: 'Towerfall Rank System' || '',
    meta: [
      { charset: 'utf-8' },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1',
      },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || '',
      },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    ],
  },
  loading: { color: '#fff' },
  css: [],
  plugins: [
    '~/plugins/vue-inject.js',
    { src: '~/plugins/tfranksystem' },
    { src: '~/plugins/snackhandler' },
  ],
  buildModules: ['@nuxtjs/vuetify', '@nuxtjs/dotenv'],
  modules: ['nuxt-material-design-icons', 'cookie-universal-nuxt'],
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },
  build: {
    extend(config, ctx) {},
  },
};
