import httplib
import datetime
from xml.dom import minidom
from django.utils.encoding import smart_str

def generate_soap(email, cal, title):
    SOAP_TEMPLATE = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
    <SendCalendarInvite xmlns="http://tempuri.org/">
    <mailRecipientAddress>%s</mailRecipientAddress>
    <mailSubject>Directions for %s</mailSubject>
    <mailBodyText>Here are the directions you requested.</mailBodyText>
    <calendarAttachmentText>%s</calendarAttachmentText>
    </SendCalendarInvite>
    </s:Body>
    </s:Envelope>"""

    soap_message = SOAP_TEMPLATE % (email, title, cal.as_string())

    # print soap_message

    webservice = httplib.HTTPConnection("calservice.apphb.com")
    webservice.putrequest("POST", "/CalendarService.svc")
    webservice.putheader("Content-Type", "text/xml")
    webservice.putheader("Content-length", "%d" % len(soap_message))
    webservice.putheader("SOAPAction", "http://tempuri.org/ICalendarService/SendCalendarInvite")
    webservice.endheaders()
    webservice.send(soap_message)

    # resp = webservice.getresponse()
    # print resp.read()

def soap_request():
    message =  """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
    <GetData xmlns="http://tempuri.org/">
    <value>0</value>
    </GetData>
    </s:Body>
    </s:Envelope>"""

    webservice = httplib.HTTPConnection("gmailservice.apphb.com")
    webservice.putrequest("POST", "/Service1.svc")
    webservice.putheader("Content-Type", "text/xml")
    webservice.putheader("Content-length", "%d" % len(message))
    webservice.putheader("SOAPAction", "http://tempuri.org/IService1/GetData")
    webservice.endheaders()
    webservice.send(message)

    resp = webservice.getresponse()
    xmldoc = minidom.parseString(resp.read())
    remaining = xmldoc.getElementsByTagName("a:NumOfRemMails")[0].childNodes[0].data
    events = xmldoc.getElementsByTagName("a:EventInfo")

    ev_list = []
    for event in events:
        dictionary = {
            'name': smart_str(event.getElementsByTagName('a:Name')[0].childNodes[0].data),
            'start': event.getElementsByTagName('a:Start')[0].childNodes[0].data,
            'location': smart_str(event.getElementsByTagName('a:Location')[0].childNodes[0].data)
        }

        ev_list.append(dictionary)

    data = {'email': event.getElementsByTagName('a:Email')[0].childNodes[0].data, 'events': ev_list, 'remaining': remaining}

    print data

    return data

    #TODO: read the events and return {'email': useremail, 'events': [{'name': eventname, 'start': startdatetime, 'location': eventlocation}]}

    #test return
    # data = {
    #         'email': 'bruno.panara+test@gmail.com', 
    #         'events': [
    #                 {
    #                     'name': 'my test event',
    #                     'start': datetime.datetime.now()+datetime.timedelta(days=1, hours=2, minutes=23),
    #                     'location': 'Buckingham Palace, London, UK'
    #                 },
    #                 {
    #                     'name': 'my second test event',
    #                     'start': datetime.datetime.now()+datetime.timedelta(days=2, hours=12, minutes=38),
    #                     'location': 'Edinburgh Castle, Edinburgh, UK'
    #                 },
    #                 {
    #                     'name': 'my third and last test event',
    #                     'start': datetime.datetime.now()+datetime.timedelta(days=1, hours=13, minutes=12),
    #                     'location': 'piccadilly station, manchester, uk'
    #                 }
    #             ]
    #         }

    # return data


