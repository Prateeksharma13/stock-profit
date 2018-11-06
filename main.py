from flask import Flask, render_template, request
app = Flask(__name__)
import requests

@app.route('/')
def homepage():
   return render_template('index.html')

@app.route('/answer',methods = ['POST', 'GET'])
def answer():
   if request.method == 'POST':
      symbol = request.form['ticker_symbol']
      r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol +'&apikey=O0VYSACAKHVTFZ1P')
      data = r.json()
      md = data['Meta Data']
      lR = md['3. Last Refreshed']
      tz = md['5. Time Zone']
      dt = lR + " " + tz
      si = data['Time Series (Daily)']
      lds = si['2018-11-05']
      osp = lds['1. open']
      csp = lds['4. close']
      sd = float(csp) - float(osp)
      url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
      result = requests.get(url).json()
      for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            company = x['name']

      cn = company
      answer = ''
      answer += 'STOCK REPORT HAS BEEN RETRIEVED FOR THE COMPANY ' + symbol
      answer += dt+"\n"
      answer += "{} ({})\n".format(cn,symbol)

      if sd < 0:
        pc = sd/float(osp) * float(100)
        answer += "{} {} ({}%)\n".format(csp,round(sd,2),round(pc,2))
      else:
        pc = sd/float(osp) * float(100)
        answer += "{} +{} (+{}%)\n".format(csp,round(sd,2),round(pc,2))
   return render_template("answer.html",p = answer)

if __name__ == '__main__':
   app.run(debug = True)

