from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

chartJson = {1: {"type": "bar", "data": [
			{"Name": "A", "Value": 5},
			{"Name": "B", "Value": 16},
			{"Name": "C", "Value": 18},
			{"Name": "D", "Value": 14},
			{"Name": "E", "Value": 11}
			]},
			 2: {"type": "col", "data": [
			 {"Name": "A", "Value": 32},
			 {"Name": "B", "Value": 23},
			 {"Name": "C", "Value": 15},
			 {"Name": "D", "Value": 10},
			 {"Name": "E", "Value": 12}
			 ]},
			 }

@app.route('/')
def index():
    """Renders index template."""
    
    return render_template('SurveyWebsite.html')

@app.route('/chart/<int:chartNumber>')
def chart(chartNumber):
	"""Returns JSON data of chart number specified."""

	return json.dumps(chartJson[chartNumber])


@app.route('/results/', methods=['POST'])
def results():
    """Saves results to text file. Redirects back to index."""

    column = request.form.get('column')
    columnSize = request.form.get('columnSize')

    print('Response Received. Column: {0}, Size: {1}'.format(column, columnSize))

    with open('results.csv','a+') as file:
        file.write('{0},{1}\n'.format(column, columnSize))

    return redirect(url_for('index'))
    

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
