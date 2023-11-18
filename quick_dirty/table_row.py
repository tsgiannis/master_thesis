#https://stackoverflow.com/questions/71877751/creating-clickable-table-that-sends-selected-row-data-as-a-post-request-to-a-fla

#https://stackoverflow.com/questions/32019733/getting-value-from-select-tag-using-flask
from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
@app.route('/')
def index():
    return render_template(
        'javascript_selected_table.html')
@app.route("/print", methods = ["post"])
def printer():
    data = request.get_json()
    print(data)

    return "hey"

if __name__=='__main__':
    app.run(debug=True)