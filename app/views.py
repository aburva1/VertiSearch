from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from computequery import Computequery
from flask import session
from flask import request

# This function fetches the query from user input, runs elastic search and displays output
@app.route('/', methods=['GET', 'POST'])
@app.route('/query', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        flash('Query requested ="%s", remember_query=%s' %
              (form.openid.data, str(form.remember_me.data)))
        cq = Computequery()
        results, time_taken, results_num = cq.fetch_results(form.openid.data)
        print "inside result()"
        print len(results)
        sorted_keys = sorted(results)
        if 'search' in request.form:
            return render_template('results.html', title='Results', results=results, keys=sorted_keys, time=time_taken, \
                               num=results_num)
        elif 'lucky' in request.form:
            key = sorted_keys[0]
            return redirect(results[key].get('docno'))
    return render_template('query.html', title='Search', form=form)


# This function makes sure the server only runs if the script is executed directly
# from the Python interpreter and not used as an imported module.
if __name__ == '__main__':
    app.run(debug=True)
