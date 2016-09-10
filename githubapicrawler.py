from flask import *
from flask import render_template
import requests
import datetime

from urlparse import parse_qs, urlparse

app = Flask(__name__)

class ApiCrawler():
    def __init__(self,urlPath):
        self.urlPath =  urlPath
        self.totalOpenIssues = []
        self.openIssues = []
        self.openMoreThan7Days = []
        self.openMoreThan24Hours = []
        self.openFor24Hours = []
        self.result = []
        self.openIssuesCount = 0
        self.openMoreThan7DaysCount = 0
        self.openMoreThan24HoursCount = 0
        self.openFor24HoursCount = 0

    def genTableData(self):
        #"https://api.github.com/repos/Shippable/support/issues?state=open"
        responseData = requests.get(self.urlPath)
        linkDict = responseData.links
        if "last" in linkDict:
            linkParam = parse_qs(urlparse(linkDict["last"]["url"]).query, keep_blank_values=True)
            totalPage = linkParam["page"][0]
            for page in range(int(totalPage)):
                pageNo = page + 1
                responseData = requests.get(
                    self.urlPath + "&page=%d" % pageNo)
                self.totalOpenIssues = self.totalOpenIssues + responseData.json()
        else:
            self.totalOpenIssues = responseData.json()

        for issue in self.totalOpenIssues:
            if 'id' in issue and 'pull_request' not in issue:
                dateTime = str(issue['created_at'])
                now = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
                issueTime = datetime.datetime.strptime(dateTime,"%Y-%m-%dT%H:%M:%SZ")
                issueTime = datetime.datetime.strptime(str(issueTime), "%Y-%m-%d %H:%M:%S")
                timeDiff = now - issueTime
                timeDiff = int(timeDiff.total_seconds() / (60 * 60))
                """Appending the data to openIssues"""
                resultDic = {}
                self.openIssuesCount +=1
                resultDic['no'] = self.openIssuesCount
                resultDic['issueId'] = issue['id'];
                resultDic['title'] = issue['title']
                resultDic['time'] = str(issueTime)
                self.openIssues.append(resultDic)
                """Appending the data where issues are opened in last 24 hours"""
                if timeDiff < 25:
                    resultDic = {}
                    self.openFor24HoursCount += 1
                    resultDic['no'] = self.openFor24HoursCount
                    resultDic['issueId'] = issue['id'];
                    resultDic['title'] = issue['title']
                    resultDic['time'] = str(issueTime)
                    self.openFor24Hours.append(resultDic)
                    """Appending the data where issues opened in last 7 days but more than 24 hours"""
                elif timeDiff > 24 and timeDiff < 169:
                    resultDic = {}
                    self.openMoreThan24HoursCount += 1
                    resultDic['no'] = self.openMoreThan24HoursCount
                    resultDic['issueId'] = issue['id'];
                    resultDic['title'] = issue['title']
                    resultDic['time'] = str(issueTime)
                    self.openMoreThan24Hours.append(resultDic)
                    """Appending the data where issues opened for more than 7 days"""
                else:
                    resultDic = {}
                    self.openMoreThan7DaysCount += 1
                    resultDic['no'] = self.openMoreThan7DaysCount
                    resultDic['issueId'] = issue['id'];
                    resultDic['title'] = issue['title']
                    resultDic['time'] = str(issueTime)
                    self.openMoreThan7Days.append(resultDic)
        self.result.append(self.openIssues)
        self.result.append(self.openFor24Hours)
        self.result.append(self.openMoreThan24Hours)
        self.result.append(self.openMoreThan7Days)

        return self.result

@app.route('/')
def hello_world():
    return render_template("index.html",title="Api Crawler")

@app.route('/listopenissues',methods=['GET','POST'])
def list_open_issues():
    repoName = str(request.form['urlValue'])
    repoName = repoName.replace("https://github.com/","")
    url = "https://api.github.com/repos/" + repoName + "/issues?state=open"
    print url
    apiObj = ApiCrawler(url)
    result = apiObj.genTableData()
    noResult = True
    if len(result[0]) or len(result[1]) or len(result[2]) or len(result[3]):
        noResult = False
    return render_template('displayresult.html',openFor24=result[1],openMore24=result[2],openMore7Day=result[3],
                           openIssues=result[0],displayEmpty=noResult)

if __name__ == '__main__':
    app.run()