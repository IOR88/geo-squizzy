from demon.gs_demon import GsDemon
from socket import AF_INET, SOCK_STREAM

# TESTING DEMON #

if __name__ == "__main__":
    demon = GsDemon(HOST='localhost',
                    PORT=6004,
                    FAMILY=AF_INET,
                    TYPE=SOCK_STREAM,
                    CONNECTIONS=3)
    demon.create_connection()
    demon.listen()