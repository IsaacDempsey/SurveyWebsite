from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    """Renders index template."""
    
    return render_template('SurveyWebsite.html')


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
