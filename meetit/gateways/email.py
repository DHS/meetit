import httplib

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

    print soap_message

    #construct and send the header

    webservice = httplib.HTTPConnection("calservice.apphb.com")
    webservice.putrequest("POST", "/CalendarService.svc")
    webservice.putheader("Content-Type", "text/xml")
    webservice.putheader("Content-length", "%d" % len(soap_message))
    webservice.putheader("SOAPAction", "http://tempuri.org/ICalendarService/SendCalendarInvite")
    webservice.endheaders()
    webservice.send(soap_message)

    # get the response

    resp = webservice.getresponse()
    print resp.read()
    # statuscode, statusmessage, header = webservice.getreply()
    # print "Response: ", statuscode, statusmessage
    # print "headers: ", header
    # res = webservice.getfile().read()
    # print res
