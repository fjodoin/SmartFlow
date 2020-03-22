# SmartFlow
Comp. Eng. Capstone project, Concordia University

## 1
Open 'events_monitoring.sh' and modify the python3 pipe PATH on line 3 so that it points to the project directory; 
> [...] | python3 /[PATH-to-project]/SmartFlow/events_parser.py

## 2
Open '/etc/filebeat/filebeat.yml' and modify the PATH on line 28 so that it points to the project directory;
> - /[PATH-to-project]/SmartFlow/smartflow_events.log

## 3
