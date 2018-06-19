#HOW To Use:
# python3 filename.py --range-number value 
#example python3 filename.py 206


#!/usr/local/bin/python3
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Parse input params.')
parser.add_argument('--range-number', dest='value', type=int, required=True,
                    help='range for number of mysqldump taken ie. filename_value.sql')

args = parser.parse_args()

#Define variables
mysqlcmd = 'mysql -u username -ppassword database_name < '
mysqlumpFileName_restore = 'mysqldump'
failure=0
value = args.value

#Go through the value range and create a mysql restore command.
for i in range(value):
    final = mysqlcmd + mysqlumpFileName_restore + str(i) + '.sql'

#Try to execute the command
    try:
        subprocess.run([final], shell=True, check=True)

#If the command fails send out the slack alert with where the restore failed
    except Exception as e:
        print (e)
        failure = 1
        failed = "The restore failed at " + mysqlumpFileName_restore + str(i)
        print (failed)
        ansible_fail = "ansible-playbook /path/to/slackrestoreupdate.yml " + \
            "--extra-vars='state=failure' -e \"message=\'" + failed + "\'\""
        
        subprocess.run([ansible_fail], shell=True, check=True)
        break

#If the restore was successful send out slack alert with success message
if failure != 1:
    success = "Restore was successful for Database DB"
    ansible_success = "ansible-playbook /path/to/slackrestoreupdate.yml " + \
        "--extra-vars='state=success' -e \"success_message=\'" + success + "\'\""

    subprocess.run([ansible_success], shell=True, check=True)

