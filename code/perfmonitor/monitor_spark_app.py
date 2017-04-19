import sys, getopt
import requests
from time import sleep
import pandas as pd
import ConfigParser
import datetime

def get_job_status(hist_base_url, appid):
    try:
        df = pd.DataFrame(columns=list(['jobid', 'submissionTime', \
                                        'completionTime', \
                                        'status', 'numTasks', 'numActiveStages', \
                                        'numCompletedStages', 'numSkippedStages', \
                                        'numFailedStages']))
        job_url = hist_base_url + "/api/v1/applications/" + appid + "/jobs"
        #print(job_url)
        response = requests.get(job_url)
        job_data = response.json()
        #print(job_data)
        rows = []
        for job in job_data:
            if 'completionTime' in job:
                rows.append({'jobid': job['jobId'], \
                             'submissionTime': job['submissionTime'], \
                             'completionTime': job['completionTime'],\
                             'status': job['status'], \
                             'numTasks':job['numTasks'], \
                             'numActiveStages':job['numActiveStages'],\
                             'numCompletedStages':job['numCompletedStages'],\
                             'numSkippedStages':job['numSkippedStages'],\
                             'numFailedStages':job['numFailedStages']})
            else:
                rows.append({'jobid': job['jobId'], \
                             'submissionTime': job['submissionTime'], \
                             'status': job['status'], \
                             'numTasks': job['numTasks'], \
                             'numActiveStages': job['numActiveStages'], \
                             'numCompletedStages': job['numCompletedStages'], \
                             'numSkippedStages': job['numSkippedStages'], \
                             'numFailedStages': job['numFailedStages']})
        df = df.append(rows)
        df.to_csv('jobs.csv')
        return
    except:
        print("error in get_job_status")
        print "Unexpected error:", sys.exc_info()[0]



def get_executor_status(hist_base_url, appid):
    try:
        df = pd.DataFrame(columns=list(['id', 'hostPort', \
                                        'isActive', \
                                        'rddBlocks', 'memoryUsed', \
                                        'diskUsed', 'totalCores',\
                                        'maxTasks', 'activeTasks', \
                                        'failedTasks', 'completedTasks',\
                                        'totalTasks', 'totalDuration', \
                                        'maxMemory']))
        exec_url = hist_base_url + "/api/v1/applications/" + appid + \
                "/allexecutors"
        #print(exec_url)
        response = requests.get(exec_url)
        exec_data = response.json()
        #print(exec_data)
        rows = []
        for executor in exec_data:
            rows.append({'id': executor['id'], \
                     'hostPort': executor['hostPort'], \
                     'isActive': executor['isActive'],\
                     'rddBlocks': executor['rddBlocks'], \
                     'memoryUsed':executor['memoryUsed'], \
                     'diskUsed':executor['diskUsed'],\
                     'totalCores':executor['totalCores'],\
                     'maxTasks':executor['maxTasks'],\
                     'activeTasks':executor['activeTasks'],\
                     'failedTasks': executor['failedTasks'], \
                     'completedTasks': executor['completedTasks'], \
                     'totalTasks': executor['totalTasks'], \
                     'totalDuration': executor['totalDuration'], \
                     'maxMemory': executor['maxMemory'] \
                     })
        df = df.append(rows)
        df.to_csv('executors.csv')
        return
    except:
        print("error in get_executor_status")
        print "Unexpected error:", sys.exc_info()[0]



def get_app_status(input_app_name, hist_base_url):

    config = ConfigParser.RawConfigParser()
    config.read('/opt/word2vec/config.properties')

    sleep(5)
    app_id = '0'
    while app_id == '0':
        app_url = hist_base_url + "/api/v1/applications"
        response = requests.get(app_url)
        data = response.json()
        for app in data:
            print(app['name'])
            if app['name'] == input_app_name:
                app_id = app['id']
                print("Got App ID. AppID = %s" % app_id)
                break
        sleep(0.5)

    #Now that the app is found, iterate till its not complete

    app_complete = 0
    app_url = hist_base_url + "/api/v1/applications/" + app_id

    df = pd.DataFrame(columns=list(['attemptid', 'completed','startTime', 'endTime']))

    while app_complete == 0:
        try:
            response = requests.get(app_url)
            appdata = response.json()
            attemptid = 0
            rows = []
            for attempt in appdata['attempts']:
                rows.append({'attemptid':attemptid, 'completed':attempt['completed'], \
                             'startTime':attempt['startTime'], 'endTime':attempt['endTime']})
                if attempt['completed'] == False:
                    get_job_status(hist_base_url, app_id)
                    get_executor_status(hist_base_url, app_id)
                    sleep(1)
                else:
                    app_complete = 1
            df = df.append(rows)
            attemptid = attemptid + 1
        except:
            print("error")
            app_complete = 1
            break
    df.to_csv('app.csv')


def get_app_status_once(input_app_name, hist_base_url):

    config = ConfigParser.RawConfigParser()
    config.read('/opt/word2vec/config.properties')

    app_url = hist_base_url + "/api/v1/applications"
    response = requests.get(app_url)
    data = response.json()
    app_id = "0"
    for app in data:
        print(app['name'])
        if app['name'] == input_app_name:
            app_id = app['id']
            print("Got App ID. AppID = %s" % app_id)

    if app_id == 0:
        print("Did not get app id")
        return

    #Now that the app is found, iterate till its not complete
    app_url = hist_base_url + "/api/v1/applications/" + app_id
    df = pd.DataFrame(columns=list(['attemptid','startTime', 'endTime']))

    try:
        response = requests.get(app_url)
        appdata = response.json()
        attemptid = 0
        rows = []
        for attempt in appdata['attempts']:
            if attempt['completed'] == True:
                rows.append({'attemptid':attemptid, \
                         'startTime':attempt['startTime'], 'endTime':attempt['endTime']})
            else:
                rows.append(
                    {'attemptid': attemptid, \
                     'startTime': attempt['startTime'],\
                     'endTime': datetime.datetime.utcnow()})
        df = df.append(rows)
        df.to_csv('app.csv')
        get_job_status(hist_base_url, app_id)
        get_executor_status(hist_base_url, app_id)
    except:
        print("error in get_app_status_once")


def get_appname_from_arg(argv):
    appname = ""
    if (len(argv) == 0):
        print 'Usage: monitor_spark_app -a <appname>'
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv, "ha:", ["appname="])
    except getopt.GetoptError:
        print 'Usage: monitor_spark_app -a <appname>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--appname"):
            appname = arg
    return appname

def main(argv):
    appname = get_appname_from_arg(argv)
    get_app_status(appname)


if __name__ == "__main__":
    main(sys.argv[1:])

