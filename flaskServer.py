from flask import Flask, render_template, request, redirect, url_for
import json
from random import shuffle
import time

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

# Start time (global)
start = time.time() 

# List of chart order. Default: [1, 2, ..., 24]
c = [i for i in range(1, 3)]


@app.route('/')
def index():
    """Renders index template."""  
   
    shuffle(c) # Randomise chart order

    return redirect('/chart/'+str(c[0]))


@app.route('/chart/<int:chartNumber>')
def chart(chartNumber):
    """Renders page containing chart of number specified.""" 

    return render_template('SurveyWebsite.html', chartNumber=chartNumber)


@app.route('/data/<int:chartNumber>')
def data(chartNumber):
    """Returns JSON data of chart number specified."""

    return json.dumps(chartJson[chartNumber])


@app.route('/results/<int:chartNumber>', methods=['POST'])
def results(chartNumber):
    """Saves results to text file. Redirects back to the next chart in list."""
    global start

    duration = time.time() - start
    start = time.time()

    column = request.form.get('column')
    columnSize = request.form.get('columnSize')

    print('Response Received. Column: {0}, Size: {1}, Duration: {2}'.format(column, columnSize, duration))

    with open('results.csv','a+') as file:
        file.write('{0},{1},{2}\n'.format(column, columnSize, duration))

    # Redirect to finish page after all charts completed.
    if c.index(chartNumber) >= (len(c) - 1):
    	return redirect(url_for('finish'))

    # Index of next chart number = (index of current element in list) + 1
    chartNumber = c[c.index(chartNumber) + 1]

    return redirect(url_for('chart', chartNumber=chartNumber))


@app.route('/finish')
def finish():
	"""Finish page. Contains button that sends you back to index."""

	return render_template('finish.html')
	
  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
