import KrakReq
import os
import time
import gevent
from gevent import monkey
def stub(*args, **kwargs):  # pylint: disable=unused-argument
    pass
monkey.patch_all = stub
from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter
from threading import Thread




currentHost = ''  
currentEndPoint = ''
currentMethod = ''
requestWaitTime = 0
guiFlag = 0
threadMode = 0


class User(HttpUser):

    global requestWaitTime
    global currentEndPoint
    global currentHost
    global currentMethod


    wait_time = between(1, requestWaitTime)
    host = "https://docs.locust.io"

    @task
    def my_task(self):
        if currentMethod == 'POST':
            #print(currentHost+currentEndPoint)
            self.client.post(currentEndPoint)
        else:
            #print(currentHost+currentEndPoint)
            self.client.get(currentEndPoint)


def start_locust(time_hour: int, time_min: int, time_sec: int, user: int, spawn_rate: int, csv_ext: str = "",endPoint: str = "",waitTime: int = 0,host: str = "",method: str = ""):
    global requestWaitTime
    global currentEndPoint
    global currentHost
    global currentMethod
    global guiFlag
    global threadMode

    requestWaitTime = waitTime
    currentEndPoint = endPoint 
    currentHost = host
    currentMethod = method

    # setup Environment and Runner
    env = Environment(user_classes=[User])
    env.create_local_runner()
    
    savedFile = csv_ext.replace('/','')
    # CSV writer
    stats_path = os.path.join(os.getcwd(), "results/data_"+savedFile+"_"+method)
    csv_writer = StatsCSVFileWriter(
        environment=env,
        base_filepath=stats_path,
        full_history=True,
        percentiles_to_report=[0.50, 0.95]
    )

    if threadMode == 1:
        if guiFlag == 0:
            try:
                guiFlag = 1
                # start a WebUI instance
                env.create_web_ui(host="127.0.0.1", port=8089, stats_csv_writer=csv_writer)
                print('Starting GUI')
            except:
                print('Already Runner')
    else:
        env.create_web_ui(host="127.0.0.1", port=8089, stats_csv_writer=csv_writer)

    # start the test
    env.runner.start(user_count=user, spawn_rate=spawn_rate)

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))
    env.stats.serialize_stats()

    # start a greenlet that saves current stats to history
    gevent.spawn(stats_history, env.runner)

    # stop the runner in a given time
    time_in_seconds = (time_hour * 60 * 60) + (time_min * 60) + time_sec
    gevent.spawn_later(time_in_seconds, lambda: env.runner.quit())

    gevent.spawn(csv_writer.stats_writer) # Writing all the stats to a CSV file

    # wait for the greenlets
    env.runner.greenlet.join()

    # stop the web server for good measures
    env.web_ui.stop()

    


def prepareTestingParamter(requests,target):
    testData = []
    #time
    timeInSeconds = int(input('Test time in seconds-> '))
    timeInMinutes = int(input('Test time in Minutes-> '))
    timeInHours = int(input('Test time in Hours-> '))
    #random request time
    randomReqesutTime = int(input('Range or random request time 0 to x -> '))
    #number of vusers
    vusers = int(input('Number of virtual users -> '))
    for req in requests:
        tempUrl = req.url
        tempMethod = req.method
        tempHeaders = req.headers
        currentTempData = {'host':target,'endpoint':tempUrl,'timeinsecond':timeInSeconds,'timeinminutes':timeInMinutes,'timeinhours':timeInHours,'randomrequesttime':randomReqesutTime,'vusers':vusers,'method':tempMethod}
        testData.append(currentTempData)
    
    return testData




def entryPoint():
    target = input('Target -> ')
    manaulDiscover = int(input('Enable Manaul Discover? 0,1 -> '))
    capturedRequests = KrakReq.getRequests(target,manaulDiscover)
    testData = prepareTestingParamter(capturedRequests,target)
    return testData
    

def attackKraken(Data):
    for testData in Data:
        thread = Thread(target = start_locust, args = [testData['timeinhours'], testData['timeinminutes'], testData['timeinsecond'], testData['vusers'], 2, f"{testData['endpoint']}",testData['endpoint'],testData['randomrequesttime'],testData['host'],testData['method']])
        #start_locust(time_hour=testData['timeinhours'], time_min=testData['timeinminutes'], time_sec=testData['timeinsecond'], user=testData['vusers'], spawn_rate=2,csv_ext = f"{testData['endpoint']}",endPoint=testData['endpoint'],waitTime=testData['randomrequesttime'],host=testData['host'],method=testData['method'])
        thread.start()
        print('hera')
        

#headers-method
#entryPoint()

def changeGuiToThreadMode():
    global threadMode
    threadMode = 1

if __name__ == "__main__":
    print('''
    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⡤⣤⣄⣾⣿⣿⣿⣿⣿⣿⣷⣠⣀⣄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠙⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣬⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣼⠟⢿⣿⣿⣿⣿⣿⣿⡿⠘⣷⣄⠀⠀⠀⠀⠀
⣰⠛⠛⣿⢠⣿⠋⠀⠀⢹⠻⣿⣿⡿⢻⠁⠀⠈⢿⣦⠀⠀⠀⠀
⢈⣵⡾⠋⣿⣯⠀⠀⢀⣼⣷⣿⣿⣶⣷⡀⠀⠀⢸⣿⣀⣀⠀⠀
⢾⣿⣀⠀⠘⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⠿⣿⡁⠀⠀⠀
⠈⠙⠛⠿⠿⠿⢿⣿⡿⣿⣿⡿⢿⣿⣿⣿⣷⣄⠀⠘⢷⣆⠀⠀
⠀⠀⠀⠀⠀⢠⣿⠏⠀⣿⡏⠀⣼⣿⠛⢿⣿⣿⣆⠀⠀⣿⡇⡀
⠀⠀⠀⠀⢀⣾⡟⠀⠀⣿⣇⠀⢿⣿⡀⠈⣿⡌⠻⠷⠾⠿⣻⠁
⠀⠀⣠⣶⠟⠫⣤⠀⠀⢸⣿⠀⣸⣿⢇⡤⢼⣧⠀⠀⠀⢀⣿⠀
⠀⣾⡏⠀⡀⣠⡟⠀⠀⢀⣿⣾⠟⠁⣿⡄⠀⠻⣷⣤⣤⡾⠋⠀
⠀⠙⠷⠾⠁⠻⣧⣀⣤⣾⣿⠋⠀⠀⢸⣧⠀⠀⠀⠉⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠹⣿⣄⠀⠀⣸⡿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⠟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀Kraken V:1.1
    
    ''')

    print('''
    
        1- Iterational
        2- Threaded  
    ''')
    
    mode = int(input('Select Mode -> '))
    

    if mode == 1:
        Data = entryPoint()
        #attackKraken(Data)
        process = []
        for testData in Data:
            #thread = Thread(target = start_locust, args = [testData['timeinhours'], testData['timeinminutes'], testData['timeinsecond'], testData['vusers'], 2, f"{testData['endpoint']}",testData['endpoint'],testData['randomrequesttime'],testData['host'],testData['method']])
            start_locust(time_hour=testData['timeinhours'], time_min=testData['timeinminutes'], time_sec=testData['timeinsecond'], user=testData['vusers'], spawn_rate=2,csv_ext = f"{testData['endpoint']}",endPoint=testData['endpoint'],waitTime=testData['randomrequesttime'],host=testData['host'],method=testData['method'])
            
           
    elif mode == 2:
        
        changeGuiToThreadMode()
        Data = entryPoint()
        #attackKraken(Data)
        process = []
        for testData in Data:
            thread = Thread(target = start_locust, args = [testData['timeinhours'], testData['timeinminutes'], testData['timeinsecond'], testData['vusers'], 2, f"{testData['endpoint']}",testData['endpoint'],testData['randomrequesttime'],testData['host'],testData['method']])
            #start_locust(time_hour=testData['timeinhours'], time_min=testData['timeinminutes'], time_sec=testData['timeinsecond'], user=testData['vusers'], spawn_rate=2,csv_ext = f"{testData['endpoint']}",endPoint=testData['endpoint'],waitTime=testData['randomrequesttime'],host=testData['host'],method=testData['method'])
            print('theread start')
            currentThread = thread.start()
            process.append(currentThread)
            #thread.join()
            #print('hera')
    
    
    # for proc in process:
    #     proc.join()
    #     print('Joined')

