# -- http://blog.csdn.net/naiveloafer/article/details/9499767
import BaseHTTPServer  
import urlparse  
class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):  
    def do_GET(self):  
        #parsed_path = urlparse.urlparse(self.path)  
        #message_parts = [  
        #        'CLIENT VALUES:',  
        #        'client_address=%s (%s)' % (self.client_address,  
        #                                    self.address_string()),  
        #        'command=%s' % self.command,  
        #        'path=%s' % self.path,  
        #        'real path=%s' % parsed_path.path,  
        #        'query=%s' % parsed_path.query,  
        #        'request_version=%s' % self.request_version,  
        #        '',  
        #        'SERVER VALUES:',  
        #        'server_version=%s' % self.server_version,  
        #        'sys_version=%s' % self.sys_version,  
        #        'protocol_version=%s' % self.protocol_version,  
        #        '',  
        #        'HEADERS RECEIVED:',  
        #        ]  
        #message = '\r\n'.join(message_parts)  
        
        htmlText = "Hello"
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(htmlText)

server = BaseHTTPServer.HTTPServer(('0.0.0.0',8080), WebRequestHandler)  
server.serve_forever()
    
