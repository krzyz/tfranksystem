<template>
  <v-list-item :inactive="true">
    <div style="min-width: 2em">
      {{ player.place ? player.place + '.' : '' }}
    </div>
    <v-list-item-content>
      <v-list-item-title>{{ player.name }}</v-list-item-title>
    </v-list-item-content>
    <v-btn
      :style="{ visibility: placed ? 'visible' : 'hidden' }"
      class="ml-3 mr-1"
      x-small
      fab
      @click="$emit('upClick')"
    >
      <v-icon>mdi-menu-up</v-icon>
    </v-btn>
    <v-btn
      :style="{ visibility: placed ? 'visible' : 'hidden' }"
      x-small
      fab
      @click="$emit('downClick')"
    >
      <v-icon>mdi-menu-down</v-icon>
    </v-btn>
    <v-list-item-action @click="$emit('actionClick')">
      <v-btn icon>
        <v-icon color="grey lighten-1">{{ icon }}</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  name: 'PlayerMatchItemComponent',
  props: {
    player: {
      type: Object,
      default: function() {
        return {
          name: '',
          place: null,
        };
      },
    },
    icon: {
      type: String,
      default: 'mdi-arrow-up-drop-circle',
    },
    placed: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({}),
};
</script>
