odoo.define('website_multi.dashboard', function(require) {
'use strict';

var core = require('web.core');
var Widget = require('web.Widget');
var Dashboard = require('website.backend.dashboard')

var _t = core._t;
var QWeb = core.qweb;

Dashboard.include({
    events: {
        'click li.js_website_deshboard': 'js_website_deshboard',
    },

    init: function(parent, context) {
        this._super(parent, context);
        this.is_bound = $.Deferred();
        this.dashboards_header = ['website.dashboard_header'];
    },

    start: function() {
        var self = this;
        return this._super().then(function() {
            self.bind_menu();
        });
    },

    fetch_data: function(website_id = false) {
        var self = this;
        return this._rpc({
            route: '/website/fetch_dashboard_data',
            params: {
                date_from: this.date_from.year() + '-' + (this.date_from.month() + 1) + '-' + this.date_from.date(),
                date_to: this.date_to.year() + '-' + (this.date_to.month() + 1) + '-' + this.date_to.date(),
                'website_id': website_id,
            },
        }).done(function(result) {
            self.website_ids = result.website_ids;
            self.website = result.website;
            self.current_website = result.current_website;
            self.data = result;
            self.dashboards_data = result.dashboards;
            self.currency_id = result.currency_id;
            self.groups = result.groups;
            // self.renderElement();
        });
    },

    js_website_deshboard: function(ev){
        ev.preventDefault();
        var self = this;
        $.when(this.fetch_data($(ev.target).data('website_id'))).then(function() {
            self.$('.o_website_dashboard_content').empty();
            self.$('.o_dashboard_common').remove();
            self.render_dashboards();
            self.render_dashboards_header();
            self.render_graphs();
        });
    },

    render_dashboards_header: function() {
        var self = this;
        _.each(this.dashboards_header, function(template) {
            self.$('.o_website_dashboard_content').prepend(QWeb.render(template, {widget: self}));
        });
    },

    bind_menu: function() {
        var self = this;
        var lazyreflow = _.debounce(this.reflow.bind(this), 200);
        core.bus.on('resize', this, function() {
            if ($(window).width() < 768 ) {
                lazyreflow('all_outside');
            } else {
                lazyreflow();
            }
        });
        core.bus.trigger('resize');

        this.is_bound.resolve();
    },

    reflow: function(behavior) {
        var self = this;
        var $more_container = this.$('#website_more_container').hide();
        var $more = this.$('#website_more');

        $more.children('li').insertBefore($more_container);

        if (behavior === 'all_outside') {
            // Show list of menu items
            self.$el.show();
            this.$el.find('li').show();
            $more_container.hide();
            return;
        }

        var $toplevel_items = this.$el.find('li').not($more_container).hide();

        self.$el.show();
        $toplevel_items.each(function() {
            var remaining_space = self.$el.find('div.navbar-collapse.collapse').width() - $more_container.outerWidth();
            self.$el.find('div.navbar-collapse.collapse ul.website_tab :visible').each
            (function() {
                if($(this).parent("ul").length){
                    remaining_space -= $(this).width();
                }
            });
            if ($(this).width() >= remaining_space) {
                return false;
            }
            $(this).show();
        });
        $more.append($toplevel_items.filter(':hidden').show());
        $more_container.toggle(!!$more.children().length);

        var $toplevel = self.$el.children("ul.website_tab li:visible");
        if ($toplevel.length === 1) {
            $toplevel.hide();
        }
    }

});
});
