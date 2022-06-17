// ==UserScript==
// @name         TradingView - Remove ads
// @version      0.1
// @description  Does what it says.
// @author       DjBonadoobie
// @require      http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js
// @icon         http://keycdn.mturkcrowd.com/data/avatars/l/0/132.jpg?1452627961
// @match      https://www.tradingview.com/chart/*
// @grant        none
// @namespace https://greasyfork.org/users/81651
// ==/UserScript==

var $ = window.$;

(function() {
  'use strict';
  const checkAd = setInterval(() => {
    const adBox = $('[data-role="toast-container"]');
    if (adBox) {
      adBox.remove();
    }}, 5000);
})();
