from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
import RankU
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
    name= soup.find('a',class_="link--country-flag")
    rank=soup.find('div',class_="rank__number")
    n=re.sub('<[^>]+>', '',str(name)).strip()
    last_n=n.rfind(',')
    n=str(n[int(last_n+1):])
    r=re.sub('<[^>]+>', '',str(rank))
    about=soup.findAll('div',class_="pane-content")
    about=str(about[2:3])
    ab=str(re.findall('>.*[</div>]',about))
    ab=ab.replace(",","")
    ab=ab.replace("<p>","")
    ab=ab.replace("</p>","")
    ab=ab.replace("' '","")
    ab=ab.replace(">","")
    ab=ab[2:len(ab)-7]
    q=0
    i=0
    for i in range(0,len(ab)):
        if(ab[i]=='.'):
            q=q+1
        if(q==5):
            break
        else:continue
        about=ab[:i+1]
    if cname in n:
        rank=r
        if(rank is "None"):
            st1=uname+" is an awesome place to study."
            st2=uname+" is a bad place to study."
            rank1=RankU(st1)
            print(rank1)
            rank2=RankU(st2)
            print(rank2)
            if(rank2>rank1):
                rank="Recommended"
            else:
                rank="Not Recommended"        
        rank=rank.replace("th","")
        rank=rank.replace("rd","") 
        rank=rank.replace("st","")
        #rank=rank.replace("nd","")
        return render_template("result.html",rank=rank,uname=uname,about=about)
    else:
        return render_template("cverify.html",cname=n,uname=uname,about=about)
@app.route('/<value>')
def getvaluere(value):
    uname=value
    quote_page = "https://www.timeshighereducation.com/world-university-rankings/"+uname.replace(" ","-")
    page = requests.get(quote_page)
    soup = BeautifulSoup(page.text, 'html.parser')
    name= soup.find('a',class_="link--country-flag")
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
    rank=rank.replace("nd","")
    return render_template("result.html",rank=rank,uname=uname)
        
if __name__=='__main__':
    app.run()
    