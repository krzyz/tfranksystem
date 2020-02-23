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
        :items="playersFiltered"
        :footer-props="{
          'items-per-page-options': [10, 30, 50],
        }"
        :items-per-page="30"
        sort-by="trueskill"
        :sort-desc="true"
        class="elevation-1"
      >
        <template v-slot:item.rank="{ item }">
          <span>{{ parseFloat(item.rank).toFixed(3) }}</span>
        </template>
        <template v-slot:item.trueskill="{ item }">
          <span>{{ parseFloat(item.trueskill).toFixed(3) }}</span>
        </template>
      </v-data-table>
      <v-checkbox
        v-model="showAll"
        color="white"
        class="mx-2"
        label="Show All"
      />
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'PlayersComponent',
  data() {
    return {
      loading: false,
      showAll: false,
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
          text: 'TrueSkill (μ - 3σ)',
          align: 'left',
          sortable: true,
          value: 'trueskill',
        },
      ],
      players: [],
    };
  },
  computed: {
    playersFiltered() {
      return this.players
        .filter(
          ({ rank, sigma }) =>
            this.showAll || (rank != 25 && sigma < 8),
        )
        .map(({ player_id, name, rank, sigma }) => ({
          player_id,
          name,
          rank,
          trueskill: rank - 3 * sigma,
        }));
    },
  },
  async mounted() {
    this.loading = true;
    this.players = await this.getPlayers();
    this.loading = false;
  },
};
</script>
