<template>
  <v-layout>
    <v-flex class="text-center">
      <v-progress-circular
        v-if="loading"
        :size="100"
        color="white"
        indeterminate
      ></v-progress-circular>
      <v-data-table
        v-if="!loading"
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
      loading: false,
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
    this.loading = true;
    const players = await this.getPlayers();
    this.players = players.map(
      ({ player_id, name, rank, sigma }) => ({
        player_id,
        name,
        rank,
        rank_safe: rank - 3 * sigma,
      }),
    );
    this.loading = false;
  },
};
</script>
