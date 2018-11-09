from flask import Flask, render_template, request, redirect, url_for
import json
from random import shuffle
import time
import string

# chartDict.py holds the dictionary containing the generated chart values
from chartDict import chartDict


app = Flask(__name__)

# Start time (global)
start = time.time()

# List of chart order. Default: [1, 2, ..., 24]
c = [i for i in range(1, 25)]


@app.route('/')
def index():
    """Renders index template."""

    shuffle(c)  # Randomise chart order

    return redirect('/chart/'+str(c[0]))


@app.route('/chart/<int:chartNumber>')
def chart(chartNumber):
    """Renders page containing chart of number specified."""

    # Letters of alphabet
    letters = list(string.ascii_uppercase)

    # Number of columns/bars in chart
    data_points = len(chartDict[chartNumber]['data'])

    return render_template('SurveyWebsite.html', chartNumber=chartNumber, data_points=data_points, letters=letters)


@app.route('/data/<int:chartNumber>')
def data(chartNumber):
    """Returns JSON data of chart number specified."""

    return json.dumps(chartDict[chartNumber])


@app.route('/results/<int:chartNumber>', methods=['POST'])
def results(chartNumber):
    """Saves results to text file. Redirects back to the next chart in list."""
    global start

    duration = time.time() - start
    start = time.time()

    column = request.form.get('column')
    columnSize = request.form.get('columnSize')

    print('Response Received. Chart: {0}, Column: {1}, Size: {2}, Duration: {3}'
          .format(chartNumber, column, columnSize, duration))

    with open('results.csv','a+') as file:
        file.write('{0},{1},{2},{3}\n'.format(chartNumber, column, columnSize, duration))

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
