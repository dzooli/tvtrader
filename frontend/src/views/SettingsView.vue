<template>
    <v-container>
        <v-row justify="center">
            <v-col class="col-sm-8">
                <v-form lazy-validation v-model="Valid" ref="form">
                    <v-container class="text-center">
                        <v-text-field
                            label="Alert Feed URL:"
                            type="Text"
                            :min="5"
                            :counter="60"
                            v-model="Field_URL"
                            :rules="Rule_URL"
                        ></v-text-field>
                        <v-text-field
                            label="Alert Timeout Refresh [s]:"
                            type="Number"
                            :min="1"
                            :counter="2"
                            v-model="Field_refresh"
                            :rules="Rule_refresh"
                        ></v-text-field>
                        <v-text-field
                            label="Alert Timeout [min]:"
                            type="Number"
                            :min="1"
                            :counter="2"
                            v-model="Field_timeout"
                            :rules="Rule_timeout"
                        ></v-text-field>
                        <v-text-field
                            label="Max Alert Count:"
                            type="Number"
                            :min="1"
                            :counter="2"
                            v-model="Field_maxcount"
                            :rules="Rule_maxcount"
                        ></v-text-field>
                    </v-container>
                    <v-toolbar dense>
                        <v-row justify="space-between">
                            <v-btn color="error" @click="resetSettings()"
                                >Reset</v-btn
                            >
                            <v-btn color="success" @click="saveSettings()"
                                >Save</v-btn
                            >
                        </v-row>
                    </v-toolbar>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
export default {
    data() {
        return {
            Valid: true,
            Field_URL: this.$store.getters.wsURL,
            Field_refresh: this.$store.getters.alertRefresh,
            Field_timeout: this.$store.getters.alertTimeout,
            Field_maxcount: this.$store.getters.maxAlerts,
            Rule_URL: [
                (v) => !!v || "Alert Feed URL is required",
                (v) => v.length <= 60 || "Max 60 characters",
            ],
            Rule_refresh: [
                (v) => !!v || "Alert Timeout Refresh is required",
                (v) => v.toString().length <= 2 || "Max 2 characters",
            ],
            Rule_timeout: [
                (v) => !!v || "Alert Timeout is required",
                (v) => v.toString().length <= 2 || "Max 2 characters",
            ],
            Rule_maxcount: [
                (v) => !!v || "Max Alert Count is required",
                (v) => v.toString().length <= 2 || "Max 2 characters",
            ],
        };
    },

    created: function () {
        this.$store.subscribe((mutation, state) => {
            this.$ls.set("settings", state, 3600 * 10000);
        });
    },

    methods: {
        saveSettings() {
            this.$store.commit("setAlertTimeout", this.Field_timeout.valueOf());
            this.$store.commit("setWsURL", this.Field_URL);
            this.$store.commit("setMaxAlerts", this.Field_maxcount.valueOf());
            this.$store.commit("setAlertRefresh", this.Field_refresh.valueOf());
        },
        resetSettings() {
            console.log(this.$settings.$data);
            this.$store.commit("initialize", this.$settings.$data, true);

            this.Field_URL = this.$store.getters.wsURL;
            this.Field_refresh = this.$store.getters.alertRefresh;
            this.Field_timeout = this.$store.getters.alertTimeout;
            this.Field_maxcount = this.$store.getters.maxAlerts;
        },
    },
};
</script>
