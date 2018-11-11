from flask import Flask, render_template, request, redirect, url_for
import json
from random import shuffle
import time
import string
import inflect

from operator import itemgetter

# chartDict.py holds the dictionary containing the generated chart values
from chartDict import chartDict


app = Flask(__name__)

# Start time (global)
start = time.time()

# Inflect pack has method for converting numerals into ordinals. E.g. 1 => 1st, 2 => 2nd, ...
p = inflect.engine()

# List of chart order. Default: [1, 2, ..., 24]
c = [i for i in range(1, 25)]

# Letters of alphabet
letters = list(string.ascii_uppercase)


@app.route('/')
def index():
    """Renders index template."""

    shuffle(c)  # Randomise chart order

    return redirect('/chart/0')


@app.route('/chart/<int:chartNumber>')
def chart(chartNumber):
    """Renders page containing chart of number specified."""

    # Number of columns/bars in chart
    data_points = len(chartDict[chartNumber]['data'])

    # Random number for questions
    q1 = p.ordinal(chartDict[chartNumber]['q1'])
    q2 = chartDict[chartNumber]['q2']

    return render_template('SurveyWebsite.html', chartNumber=chartNumber, data_points=data_points, letters=letters,
                           q1=q1, q2=q2)


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

    # Sort data points of current chart by value in descending order
    data_points_sorted = sorted(chartDict[chartNumber]['data'], key=itemgetter('Value'), reverse=True)

    # Get index of column at q1 position, e.g. column with 2. highest value
    correct_column = letters.index(data_points_sorted[chartDict[chartNumber]['q1']-1]['Name'])

    # Get size of column q2
    correct_columnSize = chartDict[chartNumber]['data'][chartDict[chartNumber]['q2']-1]['Value']

    # print('Response Received. Chart: {0}, Column: {1}, Size: {2}, Duration: {3}, Correct column: {4}, '
    #       'Correct column size: {5}'
    #       .format(chartNumber, column, columnSize, duration, correct_column, correct_columnSize))

    with open('results.csv','a+') as file:
        file.write('{0},{1},{2},{3},{4},{5}\n'.format(chartNumber, column, columnSize, duration,
                                                  correct_column, correct_columnSize))
    if chartNumber == 0:
        chartNumber = c[c.index(1)]
    else:
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
