from flask import Flask
from flask_ask import Ask, statement, question, session
from awshandle import EC2Manager

app = Flask(__name__)
ask = Ask(app, "/")

ec2_manager = EC2Manager()
server_name_list = ec2_manager.get_all_server_names()


@ask.launch
def server_handler_app():
    return question('Hi there !! I am your server manager. Currently you have %s active servers. '
                    'Would you like me to list them ?' % ec2_manager.get_active_instance_count())


@ask.intent('YesIntent')
def list_servers():
    return question('Following are the names of active servers. %s. Thats all. Would you like \
                    to do something else ?' % ','.join(ec2_manager.get_active_instance_names()))


@ask.intent('CountIntent')
def count_active_servers():
    return question('There are currently %s active servers.' % ec2_manager.get_active_instance_count())


@ask.intent('ListIntent')
def list_active_servers():
    return question('Following are the names of active servers. %s' % '\n'.join(ec2_manager.get_active_instance_names()))


@ask.intent('StartServerIntent', mapping={'server_name': 'server_name'})
def start_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name not in server_name_list:
        return question('%s is not available.Server is already started.Please try once more' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))
    else:
        ec2_manager.start_server(server_name)
        return question('%s server is ready to serve' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))


@ask.intent('StopServerIntent', mapping={'server_name': 'server_name'})
def stop_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if self.get('State', {}).get('Name') == 'stopped':
        return question('%s is not available.Server is already stopped.Please try once more' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))
    else:
        ec2_manager.stop_server(server_name)
        return question('%s server has stopped' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))

@ask.intent('MonitorIntent')
def monitor_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name in server_name_list:
        return question('%s is already being monitored' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))
    else:
        ec2_manager.monitor_server(server_name)
        return question('%s server is ready to monitor' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))


@ask.intent('UnmonitorIntent')
def unmonitor_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name in server_name_list:
        return question('%s is already unmonitored. Please try once more' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))
    else:
        ec2_manager.unmonitor_server(server_name)
        return question('%s server is getting unmonitored' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))

@ask.intent('RebootIntent')
def reboot_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name not in server_name_list:
        ec2_manager.reboot_server(server_name)
        return question('%s server is getting rebooted' % str(ec2_manager.get_active_instance_names()).replace("]","").replace("[","").replace("'",""))
    	
@ask.intent('AMAZON.CancelIntent')
def cancel_request():
    return statement('Always a pleasure working for you. Have a good day')

@ask.intent('AMAZON.StopIntent')
def stop_app():
    return statement('Always a pleasure working for you. Have a good day')
   

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)
