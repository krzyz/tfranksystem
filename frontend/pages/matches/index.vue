<template>
  <v-layout>
    <v-flex class="text-center">
      <v-progress-circular
        v-if="loading"
        :size="100"
        color="white"
        indeterminate
      ></v-progress-circular>
      <v-data-iterator
        v-if="!loading"
        :items="matches"
        :items-per-page.sync="matchesPerPage"
        :page="page"
        sort-by="datetime"
        :sort-desc="true"
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
                <v-card-title class="subheading font-weight-bold">{{
                  $moment(match.datetime).format('YYYY-MM-DD HH:mm')
                }}</v-card-title>

                <v-divider></v-divider>

                <v-list dense>
                  <v-list-item
                    v-for="(item, i) in match.teams"
                    :key="i"
                  >
                    <div class="mr-2">{{ match.ranks[i] }}.</div>
                    <v-list-item-content class="align-end">
                      {{
                        item.players
                          .map(player => player.name)
                          .join(', ')
                      }}
                    </v-list-item-content>
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
export default {
  name: 'PlayersComponent',
  data() {
    return {
      loading: false,
      page: 1,
      matchesPerPage: 4,
      matches: [],
    };
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.matches.length / this.matchesPerPage);
    },
  },
  async mounted() {
    this.loading = true;
    this.matches = await this.getMatches();
    this.loading = false;
  },
  methods: {
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1;
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1;
    },
  },
};
</script>
