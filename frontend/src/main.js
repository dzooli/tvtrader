import Vue from "vue";
import "./plugins/axios";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import storage from "./plugins/localstorage";
import toast from "vuetify-snackbar-toast";

Vue.config.productionTip = false;
Vue.prototype.$settings = new Vue({
    data: {
        devmode: true,
        alertTimeout: 15, // timeout for the alert in minutes
        alertUpdateTime: 5, // timeout update interval in seconds
        alertTimer: undefined,
        maxAlerts: 10,
        wsURL: process.env.WEBSOCKET_URL || "ws://localhost:8089/wsalerts",
        alerts: [],
    },
});

Vue.use(toast);

new Vue({
    router,
    storage,
    store,
    vuetify,
    render: (h) => h(App),
}).$mount("#app");
