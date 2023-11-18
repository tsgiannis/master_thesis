#https://stackoverflow.com/questions/32019733/getting-value-from-select-tag-using-flask
from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'name':'red'}, {'name':'green'}, {'name':'blue'}])

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    return(str(select)) # just to see what select is

if __name__=='__main__':
    app.run(debug=True)