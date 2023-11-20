from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = 'clave_secreta'

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

