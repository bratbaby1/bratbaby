/**
 * This file defines HeaderView which basically shows the header bar with search input
 * and handles showing the result of the search for artists
 */
window.HeaderView = Backbone.View.extend({
    el: '#header',
    SEARCH_FIELD_SELECTOR: "#searchText",

    initialize: function () {
        // define search result and the view for showing the results
        this.searchresultsView = new SearchListView({input_id: '#searchText'});
        // render the header section in init
        this.render();
    },

    render: function () {
        $(this.el).html(this.template());
        $('.navbar-search', this.el).append(this.searchresultsView.render().el);
        return this;
    }
});