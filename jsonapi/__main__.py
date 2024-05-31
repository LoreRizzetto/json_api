import http.server

from . import RequestRouter


def main():
    srv = http.server.HTTPServer(("", 8081), RequestRouter)
    srv.serve_forever()


if __name__ == "__main__":
    exit(main())
