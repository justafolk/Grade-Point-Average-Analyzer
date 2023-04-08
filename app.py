from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def mainapp():
    return render_template('index.html')


@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8080, debug=True)    
