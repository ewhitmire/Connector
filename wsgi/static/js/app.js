App = Ember.Application.create();

App.Router.map(function() {
	this.resource('about');
	this.resource('login');
	this.resource('jobs');
});

/*
Apps.JobsRoute  = Ember.Route.extend({
	model: function() {
		return jobs;
	}
});

var jobs = [{
	id: '1',
	title: "Graduation Photography Photos",
	author: { name: "Joe"},
	date: new Date('1-28-2014'),
	price: "$30",
	excerpt: "I offer a range of services that include portraits.  We can dicuss locations."
	body:"Something in with more description."
}, {
	id: '2',
	title: "Website",
	author: { name: "Jane"},
	date: new Date('1-29-2014'),
	price: "$30",
	excerpt: "Easy to use club websites!"
	body:"Something in with more description."
}];
*/