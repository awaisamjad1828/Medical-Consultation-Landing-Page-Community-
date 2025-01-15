from django.http import HttpResponse

 
def handler404(request,exception):
    return HttpResponse('<h1>404 error</h1>')
