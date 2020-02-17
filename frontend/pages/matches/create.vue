<template>
  <v-layout>
    <v-overlay :value="loading">
      <v-progress-circular
        :size="100"
        color="white"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <v-btn class="mr-4" @click="submit">Add match</v-btn>
          </v-row>
          <v-row justify="center">
            <v-switch v-model="teamMatch" label="Teams"></v-switch>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <v-menu
              v-model="menu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="date"
                  label="Match date"
                  prepend-icon="event"
                  readonly
                  class="mr-4"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="date"
                @input="menu = false"
              ></v-date-picker>
            </v-menu>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <v-menu
              ref="menu"
              v-model="menu2"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="time"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="time"
                  label="Match time"
                  prepend-icon="access_time"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                v-if="menu2"
                v-model="time"
                @click:minute="$refs.menu.save(time)"
              ></v-time-picker>
            </v-menu>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <v-card class="ma-2 pa-2" min-width="200">
              <v-card-title>
                Match standings
              </v-card-title>
              <v-list>
                <v-list-item-group>
                  <playerMatchItem
                    v-for="player in participants"
                    :key="player.player_id"
                    :player="player"
                    :placed="true"
                    icon="mdi-minus"
                    @actionClick="
                      movePlace(player, moveToNonParticipants)
                    "
                    @upClick="movePlace(player, participantMoveUp)"
                    @downClick="
                      movePlace(player, participantMoveDown)
                    "
                  />
                </v-list-item-group>
                <v-divider class="mx-4" />
                <v-subheader>Available players</v-subheader>
                <v-list-item-group>
                  <playerMatchItem
                    v-for="player in nonParticipants"
                    :key="player.player_id"
                    :player="player"
                    :placed="false"
                    icon="mdi-plus"
                    @actionClick="
                      movePlace(player, moveToParticipants)
                    "
                  />
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-layout>
</template>

<script>
import playerMatchItem from '../../components/matches/playerMatchItem';

export default {
  middleware: 'authenticated',
  name: 'CreateMatchComponent',
  components: {
    playerMatchItem,
  },

  data: () => ({
    players: [],
    date: new Date().toISOString().substr(0, 10),
    time: `${new Date()
      .getHours()
      .toString()
      .padStart(2, '0')}:${new Date()
      .getMinutes()
      .toString()
      .padStart(2, '0')}`,
    menu: false,
    menu2: false,
    teamMatch: false,
    loading: false,
  }),
  computed: {
    participants() {
      return this.players
        .filter(player => player.place !== null)
        .sort((a, b) => a.place - b.place);
    },
    nonParticipants() {
      return this.players.filter(p => p.place === null);
    },
    lastPlace() {
      return Math.max.apply(
        Math,
        this.players
          .map(function(p) {
            return p.place;
          })
          .concat([0]),
      );
    },
  },
  async mounted() {
    const playersList = await this.getPlayers();
    this.players = playersList.map(player => ({
      ...player,
      place: null,
    }));
  },
  methods: {
    movePlace(player, placeStrategy) {
      const foundIndex = this.players.findIndex(
        p => p.player_id === player.player_id,
      );
      player.place = placeStrategy(player.place);
      this.$set(this.players, foundIndex, player);
    },
    participantMoveDown(place) {
      return place + 1;
    },
    participantMoveUp(place) {
      if (place > 1) {
        return place - 1;
      } else {
        return place;
      }
    },
    moveToNonParticipants(place) {
      return null;
    },
    moveToParticipants(place) {
      if (this.teamMatch) {
        return Math.max(this.lastPlace, 1);
      }
      return this.lastPlace + 1;
    },
    getTeamsTeamMatch(playerGroup) {
      const grouped = playerGroup.reduce((acc, player) => {
        if (!acc[player.place]) acc[player.place] = [];
        acc[player.place].push(player.player_id);
        return acc;
      }, {});
      const groupedMap = new Map(Object.entries(grouped));
      return {
        teams: [...groupedMap.values()],
        ranks: [...groupedMap.keys()],
      };
    },
    getTeamsFreeForAll(playerGroup) {
      return {
        teams: playerGroup.map(player => [player.player_id]),
        ranks: playerGroup.map(player => player.place),
      };
    },
    async submit() {
      this.loading = true;
      const { teams, ranks } = this.teamMatch
        ? this.getTeamsTeamMatch(this.participants)
        : this.getTeamsFreeForAll(this.participants);

      const dateString = `${this.date} ${this.time}`;

      const date = new Date(
        Date.parse(dateString, 'yyyy-MM-dd HH:mm'),
      ).toISOString();

      const body = {
        teams,
        ranks,
        date,
      };

      if (ranks.length > 1) {
        await this.createMatch(body);
      } else {
        this.showMessage({
          message: 'Empty match player list!',
          color: 'warning',
        });
      }
      this.loading = false;
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
.btn-toggle {
  flex-direction: column;
}
</style>
