This script was created to take mysqldump from a mysql server which does not have python mysql connectivity.   
This script takes dumps of the database in parts (ie the database is broken down in parts based on tables and value which you decide it neeeds to be broken down into) and it avoids error which maybe caused due to interactivetimeout for mysql.   

Tools Required: python3, ansible  
Python Packages Required: numpy,   
File Required: A file which contains the list of tables   