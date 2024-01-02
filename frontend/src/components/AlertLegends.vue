<template>
    <v-row align="center" justify="center" class="ma-4">
        <v-label
            >Color codes:
            <v-chip class="sell ma-1" pill>Sell action</v-chip>
            <v-chip class="buy ma-1" pill>Buy action</v-chip>
            <v-chip class="closed ma-1" pill>Close action</v-chip>
            <v-chip class="invalidated ma-1" pill>Outdated</v-chip>
        </v-label>
    </v-row>
</template>

<script>
export default {};
</script>

<style scoped>
.sell {
    background-color: crimson !important;
}
.buy {
    background-color: forestgreen !important;
}
.closed {
    background-color: orange !important;
}
.invalidated {
    background-color: darkgrey !important;
}
</style>
