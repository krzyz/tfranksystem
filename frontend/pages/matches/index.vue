<template>
  <v-layout>
    <v-flex class="text-center">
      <v-data-iterator
        :items="matches"
        :items-per-page.sync="matchesPerPage"
        hide-default-footer
      >
        <template v-slot:default="props">
          <v-row>
            <v-col
              v-for="match in props.items"
              :key="match.match_id"
              cols="12"
              sm="6"
              md="4"
              lg="3"
            >
              <v-card>
                <v-card-title class="subheading font-weight-bold">{{ $moment(match.datetime).format('YYYY-MM-DD HH:mm') }}</v-card-title>

                <v-divider></v-divider>

                <v-list dense>
                  <v-list-item
                    v-for="(item, i) in match.teams"
                    :key="i"
                  >
                    <v-list-item-content class="align-end">{{ item.players.map(player => player.name).join(', ') }}</v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-col>
          </v-row>
        </template>

      </v-data-iterator>
    </v-flex>
  </v-layout>
</template>

<script>
  import { getMatches} from '../../services/tfranksystem';

  export default {
    name: 'players-component',
    data() {
      return {
        matchesPerPage: 4,
        matches: [],
      }
    },
    async mounted() {
      this.matches = await getMatches();
    }
  }
</script>