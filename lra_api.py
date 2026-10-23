#!/usr/bin/env python3
"""
LRA API Server — HTTP wrapper per Lino Research Assistant.
Espone /research (POST) e /health (GET).
Solo Python standard library: nessuna dipendenza esterna.
"""
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lra

HOST = '0.0.0.0'
PORT = 8080


class LRAHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"[LRA-API] {args[0] if args else fmt}")

    def _send(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self._send(200, {
                'service': 'LRA API',
                'version': '1.0',
                'status': 'ok',
                'endpoints': {
                    'POST /research': 'Genera una nota di ricerca da JSON {query, sources}',
                    'GET /health': 'Health check'
                }
            })
        else:
            self._send(404, {'error': 'not found'})

    def do_POST(self):
        if self.path != '/research':
            self._send(404, {'error': 'not found'})
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode('utf-8'))

            if 'sources' not in data:
                self._send(400, {'error': 'missing "sources" field'})
                return

            note = lra.build_note(data)
            self._send(200, {
                'ok': True,
                'note': note,
                'query': data.get('query', ''),
                'sources_count': len(data.get('sources', []))
            })
        except json.JSONDecodeError:
            self._send(400, {'error': 'invalid JSON'})
        except Exception as e:
            self._send(500, {'error': str(e)})


def main():
    server = HTTPServer((HOST, PORT), LRAHandler)
    print(f"[LRA-API] Listening on {HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[LRA-API] Shutting down")
        server.shutdown()


if __name__ == '__main__':
    main()
