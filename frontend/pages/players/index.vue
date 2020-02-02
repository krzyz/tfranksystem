<template>
  <v-layout>
    <v-flex class="text-center">
      <v-data-table
        :headers="headers"
        :items="players"
        :items-per-page="5"
        class="elevation-1"
      ></v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
  import { getPlayers } from '../../services/tfranksystem';

  export default {
    name: 'players-component',
    data() {
      return {
        headers: [
          {
            text: 'Player Name',
            align: 'left',
            sortable: true,
            value: 'name',
          },{
            text: 'Ranking',
            align: 'left',
            sortable: true,
            value: 'rank',
          },
        ],
        players: [{'name': 'nm', 'rank': 25}, {'name': 'z', 'rank': 25}],
      }
    },
    async mounted() {
      this.players = await getPlayers();
    }
  }
</script>