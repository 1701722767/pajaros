from http.server import BaseHTTPRequestHandler, HTTPServer
from prediccion import prediccion
import socketserver
import json
import cgi
import cv2
import base64
import numpy as np
from requests_toolbelt.multipart import decoder
import io, base64
from PIL import Image
import os


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}, ensure_ascii=False).encode('utf8'))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            imgPrev=fields['imagen'][0]
            z = imgPrev[imgPrev.find('/9'):]
            img = Image.open(io.BytesIO(base64.b64decode(z))).save('cache.jpg')
            imagenPrueba=cv2.imread("cache.jpg",0)
            os.remove("cache.jpg")
            categorias=['americano','basket','beisball','boxeo','ciclismo','f1','futbol','golf','natacion','tenis']
            reconocimiento=prediccion()
            indiceCategoria=reconocimiento.predecir(imagenPrueba)
            print("La imamgen cargada es ",categorias[indiceCategoria])
            message={}
            message['prediccion'] = categorias[indiceCategoria]
        
            # send the message back
            self._set_headers()
            self.wfile.write(json.dumps(message, ensure_ascii=False).encode('utf8'))

        

       
      
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('192.168.1.9', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port %d...',port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()