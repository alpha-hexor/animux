from datetime import datetime,date

def watch_log(name,ep_number,last_ep):
    '''
    function to create a watch log
    '''
    
    current_date = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open("watch_log.txt","a") as f:
        f.write("["+str(current_date) + ":" + current_time + "] Starting " + name+": episode-"+ep_number+":"+str(last_ep)+"\n")
    f.close()
