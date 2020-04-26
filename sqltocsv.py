import sys, getopt
import json, csv
import configparser
import os, logging, logging.handlers

sys.path.insert(1,'../python-ucmapi/build/lib/')
from ucmapi import Axl

configfile = 'cucmconfig.ini'
delimiter = 'comma'
sqlfile = ''
outfile = ''
version = ''
cucmserver = ''
username = ''
password = ''

def main(argv):
       global sqlfile, outfile, version, delimiter, logger
       logger = logging.getLogger()
       logging.basicConfig(handlers=[logging.handlers.RotatingFileHandler('sqltocsv.log', maxBytes=1000000, backupCount=10)],
              format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
       consolelog = logging.StreamHandler()
       consolelog.setLevel(logging.CRITICAL)
       logger.addHandler(consolelog)
       logger.critical("sqltocsv version 1.02")
       logger.critical('log level set to INFO')

       logger = logging.getLogger()
       #consolelog = logging.getLogger('console')

       try:
              opts, args = getopt.getopt(argv,"hs:o:v:d:l",["help","sql=","out=","version=","delimiter=","loglevel="])
       except:
              logger.critical('FATAL ERROR')
              logging.critical('sqltocsv.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>')
              sys.exit()
       else:
              for opt, arg in opts:
                     if opt in ('-h', "--help"):
                            logger.critical('FATAL ERROR')
                            logger.critical('sqltocsv.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>')
                            sys.exit()
                     elif opt in ("-s", "--sql"):
                            sqlfile = arg
                            logger.info('sql file is ' + sqlfile)
                            #consolelog.info('test')

                     elif opt in ("-o", "--out"):
                            outfile = arg
                            logger.info('output file is ' + outfile)
                     elif opt in ("-v", "--version"):
                            version = arg
                            logger.info('CUCM version ' + version)
                     elif opt in ("-d", "--delimiter"):
                            delimiter = arg
                     elif opt in ("-i", "--loglevel"):
                            loglevel = arg.upper()
                            logger.info('log level requested is ' + loglevel)
                            if loglevel == 'DEBUG':
                                   logger.setLevel(logging.DEBUG)
                            elif loglevel == 'INFO':
                                   logger.setLevel(logging.INFO)
                            elif loglevel == 'WARNING':
                                   logger.setLevel(logging.WARNING)
                            elif loglevel == 'ERROR':
                                   logger.setLevel(logging.ERROR)
                            elif loglevel == 'CRITICAL':
                                   logger.setLevel(logging.CRITICAL)
                            else:
                                   logger.critical('FATAL ERROR')
                                   logger.critical('valid log level values are DEBUG, INFO, WARNING, ERROR, and CRITICAL')
                                   sys.exit()
                            logger.critical('log level changed to ' + loglevel)
                     else:
                            logger.critical('FATAL ERROR')
                            logger.critical('sqltocsv.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>')
                            sys.exit()
       if sqlfile != '' and outfile != '':
              if os.path.isfile(configfile):
                     readconfigfile(configfile)
                     if cucmserver != '' and username != '' and password != '':
                            file = open(sqlfile, "r")
                            sqlquery = file.read()
                            logger.critical('SQL Query = ' + sqlquery)
                            sendsql(sqlquery)
                     else:
                            logger.critical('config cucmconfig.ini file required as below')
                            logger.critical('')
                            logger.critical('[cucm]')
                            logger.critical('server = cucmaxlserver.domain.suffix')
                            logger.critical('username = cucmaxluser')
                            logger.critical('password = cucmaxlpassword')
              else:
                     logger.critical('config cucmconfig.ini file required as below')
                     logger.critical('')
                     logger.critical('[cucm]')
                     logger.critical('server = cucmaxlserver.domain.suffix')
                     logger.critical('username = cucmaxluser')
                     logger.critical('password = cucmaxlpassword')

       else:
              logger.critical('sqltocsv.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>')

def sendsql(sqlquery):
       global outfile
       wsdlpath = 'cucmversion/' + version + '/AXLAPI.wsdl'
       logger.info('wsdlpath = ' + wsdlpath)
       axl = Axl(host=cucmserver, user=username, password=password,
                 wsdl=wsdlpath, verify=False)
       logger.critical('')
       results = axl.sql_query(sqlquery)
       logger.critical('')
       logger.debug('SQL Results')
       logger.debug(results)
       file_out = open(outfile,'w', newline='')

       if delimiter == 'tab':
              logger.critical('Writing tab delimited file')
              outwriter = csv.writer(file_out, delimiter='\t')
       else:
              logger.critical('Writing csv file')
              outwriter = csv.writer(file_out)
       rownum = 0
       for row in results:
              if rownum == 0:
                     header = row.keys()
                     outwriter.writerow(header)
                     logger.info(header)
                     rownum += 1
              outwriter.writerow(row.values())
              logger.info(row.values())
       file_out.close()

def readconfigfile(configfile):
       global cucmserver, username, password, logger
       config = configparser.ConfigParser()
       config.read('cucmconfig.ini')
       cucmserver = config['cucm']['server']
       username = config['cucm']['username']
       password = config['cucm']['password']
       logger.info('cucmserver = ' + cucmserver)
       logger.info('username = ' + username)
       logger.info('password = ' + password)

if __name__ == "__main__":
       main(sys.argv[1:])
