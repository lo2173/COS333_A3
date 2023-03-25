#-----------------------------------------------------------------------
# Author: Lois I Omotara 
# runserver.py
#-----------------------------------------------------------------------
import sys 
import reg
import argparse

def main(): 
    parser= argparse.ArgumentParser(prog='runserver.py', 
        usage='runserver.py[-h] port', 
        description='The registrar application')
    parser.add_argument('port',
        help='the port at which the server should listen',
        type=int)
    args = parser.parse_args()
    port = args.port
    try: 
        reg.app.run(host='0.0.0.0', port=port)
    except Exception as ex: 
        print(ex,file=sys.stderr)
        sys.exit(1)