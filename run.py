import argparse

from perceval import create_app

if __name__ == '__main__':

    # On récup les args liés à l'instance a créer
    parser = argparse.ArgumentParser(description="PercEval")
    parser.add_argument("instance",metavar="INSTANCE_DIRECTORY", type=str, help="Instance's directory")
    parser.add_argument("-i","--ip",type=str, help="IP's server",default="127.0.0.1")
    parser.add_argument("-p","--port", type=int, help="port",default="8080")
    args = parser.parse_args()

    app = create_app(args.instance,"http://"+args.ip+":"+str(args.port))

    app.run(host=args.ip,port=args.port)
