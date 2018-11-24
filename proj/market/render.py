from io import BytesIO
from django.http import HttpResponse,FileResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings
import os


def render_to_pdf(path,dic):
    #print "hello"
    template = get_template(path)
    html = template.render(dic)
    response = BytesIO()

    #pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), response)
    pdf = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
        path=path.replace("/","\\")
        path=path.replace("%20"," ")
        print path
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    print path
    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path