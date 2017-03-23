#!/usr/bin/python3
"""
    ClaseAppAnotado
    Aplicacion que guarda en un diccionario el documento html de una peticion
    a un servidor web externo a localhost, en el documento html viene como primera
    linea enlace a la URL original, y una de actualizacion que vuelve a pedir el html
"""
import webapp

class cacheAppAnotado(webapp.webApp):

    diccUrl = {}

    def html(self, htmlbody):
        return ("<!DOCTYPE html><html> " + htmlbody + "</html>")

    def parse(self, request):
        request = request.decode('utf-8')
        method = request.split()[0]
        recurso = request.split()[1][1:] #Lo obtengo sin barra ya que luego necesito que luego hare un find
        return (method,recurso)

    def generoHtml(self, url, rec):
        import urllib.request
        try:
            with urllib.request.urlopen(url) as f:
                html = f.read()
                html = html.decode('utf-8')
                offsite = html.find("<body")
                offsite2 = html.find(">",offsite)
                offsite2 = offsite2 + 1
                link1 = "\n<a href='" + url + "'> Original Web</a>"
                link2 = "\n<a href='/reload/" + rec + "'> RecargarWeb </a>"
                html = html[:offsite2] + link1 + link2  + html[offsite2:]
                print(html)
        except urllib.error.URLError:
            html = self.html("No ha sido posible tener conexion con " + url)
        return html

    def process(self, parsedRequest):
        method, recurso = parsedRequest
        if (method == 'GET'):
            if(recurso.find("/") == -1):
                url = "http://" + recurso
                httpCode = "200 Ok"
                if (url in self.diccUrl):
                    htmlAnswer = self.diccUrl[url]
                else:
                    htmlAnswer = self.generoHtml(url,recurso)
                    self.diccUrl[url] = htmlAnswer
            else:
                print(recurso.split("/"))
                httpCode = "200 Ok"
                htmlAnswer = self.generoHtml(url, recurso)
                self.diccUrl[url] = htmlAnswer
        else:
            httpCode = "400 Bad Request"
            htmlAnswer = self.html("Lo siento, no se puede hacer POST, PUT ni DELETE")

        return(httpCode, htmlAnswer)

if __name__ == "__main__":
    testApp = cacheAppAnotado('localhost',1231)
