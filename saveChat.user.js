// ==UserScript==
// @name     SaveChat
// @version  0.9.1
// @match    http://mush.vg/*
// @match    http://mush.vg/#
// @exclude  http://mush.vg/tid/forum
// @exclude  http://mush.vg/theEnd/*
// @exclude  http://mush.vg/expPerma/*
// @match    http://mush.twinoid.com/*
// @match    http://mush.twinoid.com/#
// @exclude  http://mush.twinoid.com/tid/forum
// @exclude  http://mush.twinoid.com/theEnd/*
// @exclude  http://mush.twinoid.com/expPerma/*
// @match    http://mush.twinoid.es/*
// @match    http://mush.twinoid.es/#
// @exclude  http://mush.twinoid.es/tid/forum
// @exclude  http://mush.twinoid.es/theEnd/*
// @exclude  http://mush.twinoid.es/expPerma/*
// ==/UserScript==

var console = unsafeWindow.console;
var Main = unsafeWindow.Main;
var $ = unsafeWindow.$;

Main.SaveChat = {};
Main.SaveChat.k = $('#cdStdWall').find(".wall .unit").last().attr("data-k");

//Tout charger
Main.SaveChat.loadMoreWall = function() {
	$('#chatBlock').scrollTop($('#chatBlock')[0].scrollHeight);
};

Main.SaveChat.afterWallLoad = function() {
	var datak = $('#cdStdWall').find(".wall .unit").last().attr("data-k");
	if(datak == Main.SaveChat.k) {
		alert('Mur chargé !');
		$('#chatBlock').attr('onscroll', "Main.onChatScroll( $(this) ); return true;");
	}
	else {
		// Load more
		Main.SaveChat.k = datak;
		Main.SaveChat.loadMoreWall(datak);
	}
};

$('<div>').html("<div class='butright'><div class='butbg'>Charger tout le canal général</div></div>").addClass('but').appendTo($('body')).bind('click', function() {
	$('#chatBlock').attr('onscroll', "Main.onChatScroll( $(this) ); if (Main.lmwProcessing) { var chatloading = window.setInterval(function() { if (!Main.lmwProcessing) { clearInterval(chatloading); Main.SaveChat.afterWallLoad(); } }, 100); return true; }");
	Main.SaveChat.loadMoreWall();
});

//Canal général
$('<div>').html("<div class='butright'><div class='butbg'>Copier le canal général</div></div>").addClass('but').appendTo($('body')).bind('click', function() {
	var s = $('#cdStdWall').html().split("\n");
	var t = $('#chatSavingTextarea');
	t.css('display', 'block');
	t.val('');
	for (i = 0; i < s.length; i++) {
		if (/mainmessage|bubble|char|neron|buddy/.test(s[i])) {
			t.val(t.val() + s[i] + "\n");
		}
	}
	alert("Fini !");
	window.scrollTo(0, document.body.scrollHeight);
});

//Favoris
$('<div>').html("<div class='butright'><div class='butbg'>Copier les favoris</div></div>").addClass('but').appendTo($('body')).bind('click', function() {
	var s = $('#cdFavWall').html().split("\n");
	var t = $('#chatSavingTextarea');
	t.css('display', 'block');
	t.val('');
	for (i = 0; i < s.length; i++) {
		if (/mainmessage|bubble|char|neron|buddy/.test(s[i])) {
			t.val(t.val() + s[i] + "\n");
		}
	}
	window.scrollTo(0, document.body.scrollHeight);
});

//Sortie texte
$('<textarea>').css({ width: '100%', height: '300px', color: 'black', display: 'none' }).attr('id', 'chatSavingTextarea').appendTo($('body'));

//Canaux privés
var privates = ['#mushChannel', '#cdPrivate0', '#cdPrivate1', '#cdPrivate2', '#cdPrivate3', '#cdPrivate4']
for (var i = 0; i < privates.length; i++) {
	var p = $(privates[i]);
	if (p.size() < 1)
		{ continue; }

	$('<div>').html("<div class='butright'><div class='butbg'>Copier le canal privé</div></div>").addClass('but').appendTo(p).bind('click', function() {
		var s = $(this).parent().html().split("\n");
		var t = $('chatSavingTextarea');
		t.css('display', 'block');
		t.val('');
		var paragraph = false;
		for (i = 0; i < s.length; i++) {
			if (/cdBroadcastLog|cdMushLog\s+cdChatLine/.test(s[i])) {
				t.val(t.val() + "<div class='log'> ");
				paragraph = false;
			}
			else if (/cdChatLine/.test(s[i])) {
				t.val(t.val() + "<div class='message'> ");
				paragraph = true;
			}
			else if (/class=["']buddy/.test(s[i])) {
				var char = s[i].match(/>(.*)</)[1].replace(/:/, '').trim().replace(/ /, '_').toLowerCase();
				t.val(t.val() + "<div class='char " + char + "'></div> <p>" + s[i].replace(/\s+/g, ' '));
			}
			else if (/<p>/.test(s[i])) {
				t.val(t.val() + s[i].replace(/\s+/g, ' ').replace(/<p>/, ''));
			}
			else if (/<strong>/.test(s[i])) {
				t.val(t.val() + s[i].replace(/\s+/g, ' '));
			}
			else if (/class=["']ago/.test(s[i])) {
				if (paragraph) {
					t.val(t.val() + '</p>');
				}
				t.val(t.val() + ' </div>\n\n');
			}
		}
		window.scrollTo(0, document.body.scrollHeight);
	});
}
