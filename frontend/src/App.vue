<template>
    <v-app>
        <v-app-bar app>
            <NavBar />
        </v-app-bar>
        <v-main>
            <v-container fluid>
                <v-toast />
                <router-view />
            </v-container>
        </v-main>
        <v-footer app padless>
            <AlertLegends />
        </v-footer>
    </v-app>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import AlertLegends from "@/components/AlertLegends.vue";
import { VToast } from "vuetify-snackbar-toast";
export default {
    name: "App",
    data() {
        return {};
    },
    components: { NavBar, AlertLegends, VToast },
    beforeMount() {
        this.$store.commit(
            "initialize",
            this.$ls.get("settings", this.$settings.$data),
            false
        );
    },
};
</script>
