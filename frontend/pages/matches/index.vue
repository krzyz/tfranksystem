<template>
  <v-layout>
    <confirmDialog
      v-model="deleteConfirmDialog"
      text="Are you sure you want to delete match?"
      @confirm="confirmDelete()"
    />
    <v-overlay :value="deleting">
      <v-progress-circular :size="100" color="white" indeterminate />
    </v-overlay>
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
        :footer-props="{
          'items-per-page-options': [10, 20, 40, 80],
        }"
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
                <v-card-title class="subheading font-weight-bold"
                  >{{
                    $moment(match.datetime).format('YYYY-MM-DD HH:mm')
                  }}
                  <v-btn
                    v-if="
                      match.match_id === mostRecentMatchId &&
                        authorized
                    "
                    text
                    class="red--text ml-2"
                    @click="tryDeleteMatch(match.match_id)"
                    >Delete</v-btn
                  >
                </v-card-title>

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
import confirmDialog from '../../components/confirmDialog';

export default {
  name: 'MatchesPage',
  components: {
    confirmDialog,
  },
  data() {
    return {
      loading: false,
      deleting: false,
      deleteConfirmDialog: false,
      match_id_to_delete: null,
      page: 1,
      matchesPerPage: 20,
      matches: [],
    };
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.matches.length / this.matchesPerPage);
    },
    mostRecentMatchId() {
      return this.matches.reduce(
        (prev, current) =>
          prev.datetime > current.datetime ? prev : current,
        { match_id: null, datetime: null },
      ).match_id;
    },
    authorized() {
      if (this.$store.state.token) {
        return true;
      }
      return false;
    },
  },
  async mounted() {
    await this.loadMatches();
  },
  methods: {
    async loadMatches() {
      this.loading = true;
      this.matches = await this.getMatches();
      this.loading = false;
    },
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1;
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1;
    },
    tryDeleteMatch(match_id) {
      this.deleteConfirmDialog = true;
      this.match_id_to_delete = match_id;
    },
    async confirmDelete() {
      this.deleting = true;
      try {
        await this.deleteMatch(this.match_id_to_delete);
        this.deleting = false;
        this.loadMatches();
      } catch (err) {
        this.deleting = false;
      }
    },
  },
};
</script>
