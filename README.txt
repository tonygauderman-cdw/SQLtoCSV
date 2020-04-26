sqltocsv Version 1.02

Released 4/25/2020

This command line tool allows you to place an SQL query in a text file, execute it against CUCM, and write the results to a csv file.

Supported CUCM Versions:
10.0, 10.5, 11.0, 11.5, 12.0, 12.5


Required Parameters:
--version (-v)      Required - CUCM Version
--sql (-s)          Redquired - Text file with SQL statement
--out (-o)          Required - Output file
--delimiter (-d)    Optional - delimiter - tab or comma
--loglevel (-l)     Optional - loglevel DEBUG, INFO, WARNING, ERROR
Use:
sqltocsv.exe --version <cucm_major_version> --sql <file_with_sql_statement> --out <file_to_write_to>


Config File Required:
cucmconfig.ini must exist and contain the hostname/ip of an AXL server as well as axl username and password in the following format

[cucm]
server = cucmaxlserver.domain.suffix
username = cucmaxluser
password= cucmaxlpassword

Changes In 1.02
Added Logging and the command line option to set logging level

Changes In 1.01
The ability to pass the optional parameter --delimiter or -d to with the value of 'tab' to specify a tab delimited output
Changed --csv (-c) to --out (-o) to reflect multiple file formats
