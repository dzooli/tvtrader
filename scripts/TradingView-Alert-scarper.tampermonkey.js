// ==UserScript==
// @name         TradingView - Alert scarper
// @version      0.1
// @description  Does what it says.
// @require      https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js
// @author       dzooli
// @run-at       document-idle
// @match        https://www.tradingview.com/chart/*
// @grant        jQuery
// ==/UserScript==

var $ = window.jQuery;

(function() {
    'use strict';
    const checkAlert= setInterval(() => {
        const alertTimeout = 15 * 60;
        const alertBody = $("div.widgetbar-widget-alerts_log > div.widgetbar-widgetbody > div > :nth-child(2) > :nth-child(2) > div").first();
        let alertText = alertBody.contents().text().trim();
        if (alertText != "") {
            let alert = JSON.parse(alertText);
            let currTime = Date.now();
            let alrtTime = new Date(alert.timestamp);
            let alertTime = alrtTime.getTime();
            alertBody.css({
                "background": (((currTime - alertTime) / 1000) < alertTimeout) ? "red" : "gray",
            });
        }
    }, 5000);
})();
