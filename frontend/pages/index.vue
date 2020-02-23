<template>
  <v-layout>
    <v-flex class="text-center">
      <v-progress-circular
        v-if="loading"
        :size="100"
        color="white"
        indeterminate
      ></v-progress-circular>
      <div v-if="!loading">
        <v-card class="mb-10">
          <v-card-title>
            Skill
          </v-card-title>
          <v-card-content>
            <VueApexCharts
              width="100%"
              type="line"
              :options="chartOptions"
              :series="seriesSkill"
            ></VueApexCharts>
          </v-card-content>
        </v-card>
        <v-card>
          <v-card-title>
            TrueSkill
          </v-card-title>
          <v-card-content>
            <VueApexCharts
              width="100%"
              type="line"
              :options="chartOptions"
              :series="seriesTrueSkill"
            ></VueApexCharts>
          </v-card-content>
        </v-card>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import VueApexCharts from 'vue-apexcharts';

export default {
  components: {
    VueApexCharts,
  },
  data: function() {
    return {
      loading: false,
      ranksHistory: null,
      playerNamesById: {},
      chartOptions: {
        chart: {
          background: '#424242',
          id: 'ranks-chart',
        },
        colors: [
          '#c8522c',
          '#7363d4',
          '#60b64d',
          '#be57c4',
          '#bab242',
          '#6771bd',
          '#c58643',
          '#5f9ed7',
          '#d13f56',
          '#49c1b9',
          '#d54a8f',
          '#529f6b',
          '#cf8cce',
          '#727b31',
          '#964b7e',
          '#cd7171',
        ],
        stroke: {
          curve: 'smooth',
        },
        xaxis: {
          type: 'datetime',
        },
        yaxis: {
          labels: {
            formatter: value => value.toFixed(3),
          },
        },
        tooltip: {
          theme: 'dark',
        },
        theme: {
          mode: 'dark',
        },
      },
    };
  },
  computed: {
    seriesSkill() {
      if (!this.ranksHistory) return [];
      return Object.keys(this.ranksHistory).map(player_id => {
        const player_data = this.ranksHistory[player_id];
        const times = player_data.time;
        const ranks = player_data.rank;

        return {
          name: this.playerNamesById[player_id],
          data: times.map((time, i) => [time, ranks[i]]),
        };
      });
    },
    seriesTrueSkill() {
      if (!this.ranksHistory) return [];
      return Object.keys(this.ranksHistory).map(player_id => {
        const player_data = this.ranksHistory[player_id];
        const times = player_data.time;
        const ranks = player_data.rank;
        const sigmas = player_data.sigma;

        return {
          name: this.playerNamesById[player_id],
          data: times.map((time, i) => [
            time,
            ranks[i] - 3 * sigmas[i],
          ]),
        };
      });
    },
  },
  async mounted() {
    this.loading = true;
    const [ranksHistory, players] = await Promise.all([
      this.getRanksHistory(),
      this.getPlayers(),
    ]);
    this.ranksHistory = ranksHistory;
    this.playerNamesById = players.reduce((map, player) => {
      map[player.player_id] = player.name;
      return map;
    }, {});
    this.loading = false;
  },
};
</script>
