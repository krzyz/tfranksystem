<template>
  <v-layout>
    <v-flex class="text-center">
      <v-data-table
        :headers="headers"
        :items="players"
        :items-per-page="20"
        sort-by="rank"
        :sort-desc="true"
        class="elevation-1"
      >
        <template v-slot:item.rank="{ item }">
          <span>{{ parseFloat(item.rank).toFixed(3) }}</span>
        </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import { getPlayers } from '../../services/tfranksystem';

export default {
  name: 'PlayersComponent',
  data() {
    return {
      headers: [
        {
          text: 'Player Name',
          align: 'left',
          sortable: true,
          value: 'name',
        },
        {
          text: 'Ranking',
          align: 'left',
          sortable: true,
          value: 'rank',
        },
      ],
      players: [],
    }
  },
  async mounted() {
    this.players = await getPlayers();
  },
};
</script>
