from flask import Flask, render_template, request
app=Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/', methods=['POST'])
def getvalue():
    cname=request.form['cname']
    uname=request.form['uname']
    coname=request.form['coname']
    print(cname,uname,coname)
    #return render_template("result.html")
if __name__=='__main__':
    app.run()
    