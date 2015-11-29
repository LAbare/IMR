import os.path

n = input("Code de la partie : ")
f = open(n + '/main.txt', 'r')
dest = open(n + '.html', 'w')

def smileySource(string):
	return string.replace('src="//', 'src="http://').replace('src="http://data.twinoid.com/img/smile', 'src="smile').replace('src="/img', 'src="http://mush.vg/img')

ismainmessage = True
mainmessages = []
replies = []
privates = {}
cats = {}
i = -1

for line in f:
	if 'mainmessage' in line:
		ismainmessage = True
		mainmessages.append('')
		replies.append([])
		i += 1
		j = 0
	if 'class="reply bubble' in line:
		ismainmessage = False
		replies[i].append('')
	if 'class="char' in line or 'class="neron' in line:
		if ismainmessage:
			mainmessages[i] += smileySource(line.strip('\n\t'))
		else:
			replies[i][j] += smileySource(line.strip('\n\t'))
	if 'class="buddy' in line:
		if ismainmessage:
			mainmessages[i] += smileySource(line.strip('\n\t'))
		else:
			replies[i][j] += smileySource(line.strip('\n\t'))
			j += 1

for p in range(0, 1000):
	if os.path.isfile(n + '/private' + str(p) + '.txt'):
		private = open(n + '/private' + str(p) + '.txt')
		info = eval(private.readline())
		cat = info['cat']
		if cat not in cats:
			cats[cat] = [input("Nom de la catégorie [" + cat + "] : "), []]
		cats[cat][1].append('private' + str(p))

		lines = []
		for line in private:
			if line:
				lines.append(line)
		
		privates['private' + str(p)] = [info['name'], lines]
		private.close()
	else:
		break

dest.write("<!DOCTYPE html>\n<html>\n<head>\n\t<title>" + input("Nom de la partie : ") + " — Partie IMR</title>\n")
dest.write("\t<link href='style.css' rel='stylesheet' type='text/css' />\n" +
"	<meta charset='UTF-8' />\n" +
"</head>\n\n" +
"<body>\n" +
"<script>\n" +
"function show(el) {\n" +
"	var repliesblock = el.nextElementSibling;\n" +
"	if (repliesblock.className == 'hiddenreplies')\n" +
"		{ el.textContent = 'Cacher les réponses'; repliesblock.className = 'shownreplies'; }\n" +
"	else\n" +
"		{ el.textContent = 'Montrer les réponses'; repliesblock.className = 'hiddenreplies'; }\n" +
"}\n\n" +
"function changeChannel(channel) {\n" +
"	var children = document.body.children;\n" +
"	for (var i = 0; i < children.length; i++)\n" +
"		{ children[i].style.display = 'none'; }\n" +
"	document.getElementById('menu').style.display = 'block';\n" +
"	document.getElementById(channel).style.display = 'block';\n" +
"}\n\n" +
"function displaySubCat(cat) {\n" +
"	var display = false;\n" +
"	var el = document.getElementById(cat);\n" +
"	if (el.style.display == 'none')\n" +
"		{ display = true; }\n" +

"	var cats = document.getElementsByClassName('cat');\n" +
"	for (var i = 0; i < cats.length; i++)\n" +
"		{ cats[i].style.display = 'none'; }\n" +

"	if (display)\n" +
"		{ el.style.display = 'block'; }\n" +
"}\n" +
"</script>\n\n")

# MENU
dest.write("<div id='menu'>\n")
menu = "\t<span onclick='changeChannel(\"wall\");'>Canal général</span> — "
for cat in cats:
	menu += "<span onclick='displaySubCat(\"sub_" + cat + "\");'>" + cats[cat][0] + "</span> — "
menu = menu[:-3] + "\n\n"
dest.write(menu)

# SOUS-CATÉGORIES
for cat in cats:
	dest.write("\t<div class='cat' id='sub_" + cat + "'>\n")
	for priv in cats[cat][1]:
		dest.write("\t\t<div onclick='changeChannel(\"" + priv + "\");'>" + privates[priv][0] + "</div>\n")
	dest.write("\t</div>\n")

dest.write("</div>\n\n<div id='wall'>\n")

for k in range(0, len(mainmessages)):
	dest.write('\t<div class="mainmessage" id="' + str(k) + '"> ' + mainmessages[k] + '<a class="link" href="#' + str(k) + '">Ancre</a> </div>\n')
	if replies[k]:
		dest.write('\t<div class="show" onclick="show(this);">Montrer les réponses</div>\n\t<div class="hiddenreplies">\n')
		for l in range(0, len(replies[k])):
			dest.write('\t\t<div class="reply"> ' + replies[k][l] + ' </div>\n')
		dest.write('\t</div>\n')
	dest.write('\n')
dest.write('</div>\n')

# CANAUX PRIVÉS
for priv in privates:
	dest.write("<div id='" + priv + "' class='private'>\n")
	dest.write("\t<h1>" + privates[priv][0] + "</h1>\n")
	for l in privates[priv][1]:
		dest.write("\t" + l)
	dest.write("\n</div>\n\n")

dest.write("<script>\n" +
"var cats = document.getElementsByClassName('cat');\n" +
"for (var i = 0; i < cats.length; i++)\n" +
"	{ cats[i].style.display = 'none'; }\n" +
"</script>\n</body>\n</html>")
f.close()
dest.close()
