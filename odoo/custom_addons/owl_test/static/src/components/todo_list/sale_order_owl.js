/** @odoo-module **/
odoo.define('client_act.sale_cust_v2', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var SaleCustom = AbstractAction.extend({
    template: 'DashBoard.action',

    });
    core.action_registry.add("sale_cust_v2", SaleCustom);
    return SaleCustom;
 });
 