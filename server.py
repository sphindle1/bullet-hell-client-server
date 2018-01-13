from http.server import  BaseHTTPRequestHandler, HTTPServer
import sqlite3 as lite
import sys

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    con = lite.connect('users.db')
    cur = con.cursor()
    #cur.execute("CREATE TABLE Users(Name TEXT, Completed Date)")
    def do_GET(self):
        self.send_response(200)


        self.send_header('Content-type', 'text/html')
        self.end_headers()

        game = open('shooter.html', 'r').readlines()
        for line in game:
            self.wfile.write(bytes(line, "utf8"))
        return
    def do_POST(self):
        print ("do_POST() is called")
        print(self.path)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len).decode("utf8")
        name = post_body.split("=")[0]
        date = post_body.split("=")[1]
        date = date.split("+")[1:4]
        completed = date[1] + " " + date[0] + " " + date[2]
        self.cur.execute("INSERT INTO Users VALUES(\'{0}\', \'{1}\')".format(name, completed))
        self.cur.execute("SELECT * FROM Users")
        rows = self.cur.fetchall()
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("<font size = \"5\">Hall of Fame</font><br><br>", "utf8"))
        self.wfile.write(bytes("<table style=\"border: 1px solid black\"><tr> <th style=\"border: 1px solid black\">User Name</th>\
         <th style=\"border: 1px solid black\">Date Completed</th> </tr>", "utf8"))
        for row in rows:
            self.wfile.write(bytes(str("<tr><td style=\"border: 1px solid black\">" + row[0] +
            "</td>"+ "<td style=\"border: 1px solid black\">" + row[1]) + "</td></tr>", "utf8"))
        #self.wfile.write(bytes("<a href=\"website.html\">Back to Game</a>", "utf8"))
        self.wfile.write(bytes("</table><br><br><form action=\"website.html\"><input type=\"submit\" value=\"Back to game\"/></form>", "utf8"))

def run():
    print('starting server...')

    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

run()
