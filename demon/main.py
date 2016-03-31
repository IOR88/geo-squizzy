from demon.gs_demon import GsDemon

from socket import AF_INET, SOCK_STREAM
import sys

if __name__ == "__main__":
    demon = GsDemon(pid_file='/home/ing/PycharmProjects/geo-squizzy/geosquizzy/demon/logs/pid.txt',
                    std_in='/home/ing/PycharmProjects/geo-squizzy/geosquizzy/demon/logs/in.txt',
                    std_out='/home/ing/PycharmProjects/geo-squizzy/geosquizzy/demon/logs/out.txt',
                    std_err='/home/ing/PycharmProjects/geo-squizzy/geosquizzy/demon/logs/err.txt',
                    HOST='localhost',
                    PORT=7801,
                    FAMILY=AF_INET,
                    TYPE=SOCK_STREAM,
                    CONNECTIONS=3)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            demon.start()
        elif 'stop' == sys.argv[1]:
            demon.stop()
        elif 'restart' == sys.argv[1]:
            demon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)