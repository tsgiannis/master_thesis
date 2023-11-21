from flask import Flask, render_template, request, Blueprint

app = Flask(__name__)

# Blueprint definition
my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route('/route', methods=['POST'])
def route_name():
    selected_option = request.form.get('selected_option')
    # Process the selected option as needed
    return f'Selected option: {selected_option}'

app.register_blueprint(my_blueprint)

@app.route('/')
def index():
    return render_template('index_post.html')

if __name__ == '__main__':
    app.run(debug=True)