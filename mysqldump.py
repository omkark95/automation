#HOW To Use:
# python3 filename.py --range-number value 
#example python3 filename.py 206

#Packages requirements: Numpy and np

#Mysql requirement: endpoint, please mention the mysqldump filename

#!/usr/local/bin/python3
import np, subprocess, os
from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description='Parse input params.')
parser.add_argument('--range-number', dest='value', type=int, required=True,
                    help='range for number of mysqldump to take ie. filename_value.sql')

args = parser.parse_args()
value = args.value

#Open file containing the table names and strip them for spaces, new line and load them as a list
f = open("file_containing_table_names.txt",'r')
tables = []
for line in f.readlines():
    tables.append(line.strip("\n,|, "))

#Define variables
mysqlcmd = "mysqldump -h endpoint -u user -ppassword database_name"
mysqltables = ""
ansible_fail = ''
count_of_tables, count_in_split_table = 0, 0
failed_execution, success_execution, return_code, index_on_splitted_table = 0, 0, 0, 0
start_time = datetime.now()

#This would split the table list in value number of parts creating nested list
split_tables = np.array_split(tables,value)


#This would be used to break the while loop
x = None


while failed_execution != 1 or index_on_splitted_table != value-1:

#Parse the nested list to get into the inner list
    for index_on_splitted_table in range(value):


#Parse the inner list to get the table names        
        for tablename_in_split_table in split_tables[index_on_splitted_table]:
            count_in_split_table += 1
            mysqltables += " " + tablename_in_split_table

#Create a final command to run. This would create the mysqldumps.
        final = mysqlcmd + mysqltables + " > ~/filename_" + str(index_on_splitted_table) + ".sql"
        count_of_tables += count_in_split_table
 
#This would run the command.
        try:
            return_code = subprocess.run([final], shell=True, check=True)
            print ("\n" + final)
            count_in_split_table = 0
            mysqltables = ""

#This would catch the error and send the slack alert with number of tables completed and the number of tables failed. This would locally print the time taken as well.
        except Exception as e:
            x=e
            print (return_code)
            end_time = datetime.now()
            print (e)
            print ("Backup failed after %d tables" % (count_of_tables-count_in_split_table))
            for index_on_failed_table in range(index_on_splitted_table,206):
                for failed_tablename_in_split_table in split_tables[index_on_failed_table]:
                    mysqltables += " " + failed_tablename_in_split_table
            failed_message = "Failed table names are" + mysqltables + " Time taken:" + str(end_time-start_time)

            print ("Backup taken for %d" % (count_of_tables-3))
            x = "-e"
            y = "\""
            ansible_fail = "ansible-playbook /path/to/slackdumpupdate.yml " + "--extra-vars='state=failure' " + x + " " + "\"message=\'" + failed_message + "\'" + y
            print (ansible_fail)
            subprocess.run([ansible_fail], shell=True, check=True)
            break 

#This would break the while loop
    if x != None: 
        failed_execution = 1
        break
    else: continue

#This would check if the execution was successful
if failed_execution != 1: success_execution = 1

#If the execution was successful then this would send out slack alert.
if success_execution ==1:
    success_end_time = datetime.now()
    success_message = "Backup successful. Time taken:" + str(start_time-success_end_time)
    ansible_success = "ansible-playbook /path/to/slackdumpupdate.yml --extra-vars='state=success' " + \
        "-e \"success_message=\'" + success_message + "\'\""
    subprocess.run([ansible_success], shell=True)

