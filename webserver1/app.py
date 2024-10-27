import os
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer

conn = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD']
)

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        message TEXT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS request_counts (
        server_name TEXT PRIMARY KEY,
        request_count INTEGER
    )
''')

cur.execute("INSERT INTO request_counts (server_name, request_count) VALUES ('webserver1', 0) ON CONFLICT (server_name) DO NOTHING")
cur.execute("INSERT INTO request_counts (server_name, request_count) VALUES ('webserver2', 0) ON CONFLICT (server_name) DO NOTHING")
conn.commit()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        cur.execute("UPDATE request_counts SET request_count = request_count + 1 WHERE server_name = 'webserver1'")
        conn.commit()

        cur.execute("SELECT request_count FROM request_counts WHERE server_name = 'webserver1'")
        webserver1_count = cur.fetchone()[0]

        cur.execute("SELECT request_count FROM request_counts WHERE server_name = 'webserver2'")
        webserver2_count = cur.fetchone()[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = f'''
        <html>
            <head>
                <style>
                    body {{
                        display: flex;
                        height: 100vh; /* Full height */
                        margin: 0;
                    }}
                    .pune {{
                        background-color: white; /* Pune background */
                        width: 50%; /* Half of the screen */
                        padding: 20px;
                        background-color: green; /* Webserver1 serving */
                    }}
                    .hyderabad {{
                        background-color: white; /* Hyderabad background */
                        width: 50%; /* Half of the screen */
                        padding: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="pune">Pune - Requests served by Web Server 1: {webserver1_count}</div>
                <div class="hyderabad">Hyderabad - Requests served by Web Server 2: {webserver2_count}</div>
            </body>
        </html>
        '''
        self.wfile.write(response.encode())

httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
