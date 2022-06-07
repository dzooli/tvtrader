import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    alertTimeout: 10, // In minutes
    maxAlerts: 10,
    alerts: [],
  },

  getters: {
    alerts: (state) => state.alerts,
    maxAlerts: (state) => state.maxAlerts,
  },

  mutations: {
    /**
     * Add the received alert and calculate if it is already timed out.
     * Timeout value is defined in the state and given in minutes.
     *
     * @param {*} state
     * @param {*} param1
     */
    addAlert(state, { symbol, direction, timestamp }) {
      state.alerts.unshift({
        symbol: symbol,
        direction: direction,
        timestamp: timestamp,
        timedout:
          Date.now() / 1000 - timestamp > state.alertTimeout * 60
            ? true
            : false,
      });
      if (state.alerts.length > state.maxAlerts) {
        state.alerts.splice(state.alerts.length - 1, 1);
      }
    },
  },

  actions: {},

  modules: {},
});
