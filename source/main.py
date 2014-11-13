from flask import Flask, render_template, request, url_for, Markup

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

uw_flow_url = 'https://uwflow.com/course/'

instructorList = list()
instructorMapping = dict()
loaded = False

def loadData():
	global instructorMapping
	f = open('ClassesMapped', 'r')
	lines = f.readlines()
	for i in lines:
		part = i.partition('(')[0].rstrip()
		instructorMapping[part] = '(' + i.partition('(')[2]
		instructorList.append(part)

def convertName(name):
	return name.replace(',', ", ")


@app.route('/')
def main():
	global loaded
	f2 = ""
	if not loaded:
		loadData()
		loaded = True
		f2+="HERP DERP"
	for i in instructorList:
		f2+=render_template("fe.html", name=convertName(i))
	return render_template("main.html", content=f2)

@app.route('/search')
def search():
	global instructorMapping
	name = request.args['prof'].split(',')
	firstName = name[1].lstrip()
	lastName = name[0]
	classes = instructorMapping[str(request.args['prof']).replace(', ', ',')].rstrip().replace('(', '').replace(')', '').split(' ')
	classString = ""
	for i in range(0, len(classes)/4):
		classString+= render_template("class.html", course=classes[i*4], room=classes[i*4 + 1], time = classes[i*4 + 2] + ' ' + classes[i*4 + 3], courseLower = classes[i*4].lower())
	return render_template("search.html", firstName = firstName, lastName = lastName, content = classString)