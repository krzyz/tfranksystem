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
        <VueApexCharts
          width="100%"
          type="line"
          :options="chartOptions"
          :series="series"
        ></VueApexCharts>
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
          background: '#303030',
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
    series() {
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
