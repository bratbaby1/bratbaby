window.Artist = Backbone.Model.extend({

    urlRoot:"../api/people/",

    initialize:function () {
        this.list = new PersonCollection();
        this.list.url = '../api/people/' + this.id + '/path';
    }

});

window.PersonCollection = Backbone.Collection.extend({

    model: Artist,

    url:"../api/people",

    findByName:function (key) {
        var url = (key == '') ? '../api/artist' : "../api/artist/search/?query=" + key;
        console.log('findByName: ' + key);
        var self = this;
        $.ajax({
            url:url,
            dataType:"json",
            success:function (data) {
                console.log("search success: " + data.length);
                self.reset(data);
            }
        });
    }

});