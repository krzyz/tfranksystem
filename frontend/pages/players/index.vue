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
          text: 'Skill (μ)',
          align: 'left',
          sortable: true,
          value: 'rank',
        },
        {
          text: 'Skill (μ - 3σ)',
          align: 'left',
          sortable: true,
          value: 'rank_safe',
        },
      ],
      players: [],
    };
  },
  async mounted() {
    const players = await this.getPlayers();
    console.log(players);
    this.players = players.map(
      ({ player_id, name, rank, sigma }) => ({
        player_id,
        name,
        rank,
        rank_safe: rank - 3 * sigma,
      }),
    );
  },
};
</script>
