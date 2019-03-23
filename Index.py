from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
app=Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/', methods=['POST'])
def getvalue():
    cname=request.form['cname']
    uname=request.form['uname']
    #coname=request.form['coname']
    quote_page = "https://www.timeshighereducation.com/world-university-rankings/"+uname.replace(" ","-")
    page = requests.get(quote_page)
    soup = BeautifulSoup(page.text, 'html.parser')
    name= soup.find('div',class_="institution-info__contact-detail institution-info__contact-detail--address")
    rank=soup.find('div',class_="rank__number")
    n=re.sub('<[^>]+>', '',str(name)).strip()
    last_n=n.rfind(',')
    n=str(n[int(last_n+1):])
    r=re.sub('<[^>]+>', '',str(rank))
    if cname in n:
        #print(n)
        rank=r
        if rank is "o":
            rank="NA"
        rank=rank.replace("th","")
        rank=rank.replace("rd","") 
        rank=rank.replace("st","")
        return render_template("result.html",rank=rank,uname=uname)
    else:
        rank=rank.replace("th","")
        rank=rank.replace("rd","") 
        rank=rank.replace("st","")
        return render_template("cverify.html",cname=n,uname=uname)
@app.route('/<value>'   )
def getvaluere(value):
    uname=value
    quote_page = "https://www.timeshighereducation.com/world-university-rankings/"+uname.replace(" ","-")
    page = requests.get(quote_page)
    soup = BeautifulSoup(page.text, 'html.parser')
    name= soup.find('div',class_="institution-info__contact-detail institution-info__contact-detail--address")
    rank=soup.find('div',class_="rank__number")
    n=re.sub('<[^>]+>', '',str(name)).strip()
    last_n=n.rfind(',')
    n=str(n[int(last_n+1):])
    rank=re.sub('<[^>]+>', '',str(rank))
    if rank is "o":
        rank="NA"
    rank=rank.replace("th","")
    rank=rank.replace("rd","") 
    rank=rank.replace("st","")
    return render_template("result.html",rank=rank,uname=uname)
        
if __name__=='__main__':
    app.run()
    