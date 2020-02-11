<template>
  <v-layout>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <v-card class="ma-2 pa-2" min-width="200" min-height="300">
              <v-card-title>
                Match results
              </v-card-title>
              <draggable min-height="300" v-model="participants" group="people">
                <v-chip v-for="(player, i) in participants" class="pa-2 d-block ma-2">
                  <v-icon
                    @click="toggleTied(player, i)"
                    class="mr-2"
                    v-text="`mdi-numeric-${player.place}-box-${player.tied ? 'multiple-' : ''}outline`"
                  ></v-icon>
                      {{player.name}}
                </v-chip>
            </draggable>
            </v-card>
            <v-card class="ma-2 pa-2" min-width="200">
              <v-card-title>
                Available players 
              </v-card-title>
              <draggable v-model="players2" group="people">
                <v-chip v-for="(player, i) in players2" class="pa-2 d-block ma-2">
                  <v-icon class="mr-2" v-text="`mdi-account-box-outline`"></v-icon>
                  {{player.name}}
                </v-chip>
              </draggable>
            </v-card>
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
                  max-width="290px" 
                  class="mr-4"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="date" @input="menu = false"></v-date-picker>
            </v-menu>
            <v-menu
              ref="menu"
              v-model="menu2"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="time"
              transition="scale-transition"
              offset-y
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="time"
                  label="Match time"
                  prepend-icon="access_time"
                  readonly
                  v-on="on"
                  max-width="290px"
                  min-width="290px"
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
            <v-btn class="mr-4" @click="submit">Add match</v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-layout>
</template>

<script>
  import { createMatch, getPlayers } from '../../services/tfranksystem';
  import draggable from 'vuedraggable';

  export default {
    name: 'create-match-component',

    data: () => ({
      players: [],
      players2: [],
      date: new Date().toISOString().substr(0, 10),
      time: `${(new Date()).getHours().toString().padStart(2, "0")}:${(new Date()).getMinutes().toString().padStart(2, "0")}`,
      menu: false,
      menu2: false,
    }),
    methods: {
      toggleTied (player, i) {
        const newPlayers = this.players.slice();
        newPlayers[i] = {
          ...player,
          tied: !player.tied,
        };
        this.participants = newPlayers;
      },
      async submit () {
        const teams = this.participants.map(player => [ player.player_id ] );
        const ranks = this.participants.map(player => player.place);
        const dateString = `${this.date} ${this.time}`;

        const date = (new Date(Date.parse(dateString, "yyyy-MM-dd HH:mm"))).toISOString();

        const body = {
          teams,
          ranks,
          date,
        };

        if (ranks.length > 1) {
          await createMatch(body);
        }
      },
    },
    computed: {
      participants: {
        get () {
          return this.players;
        },
        set (newParticipants) {
          let tied = 0;
          this.players = newParticipants.map((player, i) => {
            if (player.tied === true) {
              tied += 1;
            } else {
              tied = 0;
            }
            return {
              ...player,
              place: Math.max(1, 1 + i - tied),
              tied: player.tied || false,
            };
          });
        },
      },
    },
    async mounted() {
      const playersList = await getPlayers();
      this.players2 = playersList.map(player => ({
        ...player,
        place: null,
        tied: false,
      }));

    },
    components: {
        draggable,
    },
  };
</script>

<style scoped>
.container {
    max-width: 500px;
}
</style>