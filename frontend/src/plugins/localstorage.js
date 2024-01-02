import Vue from "vue";
import Storage from "vue-ls";

const options = {
    namespace: "tvtrader_",
    name: "ls",
    storage: "local",
};
Vue.use(Storage, options);

export default {};
