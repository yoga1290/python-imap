def connectIMAP(username, password, imap_server, imap_port=None, most_recent_messages_count=2, subject=None, fromEmail=None, toEmail=None, OUTPUT_DIR='.'):
    
    import imaplib
    import email
    from email.header import decode_header
    # import webbrowser
    import os

    # from message_handler import messageHandler
    from . import message_handler
    
    # create an IMAP4 class with SSL 
    if imap_port:
        imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    else:
        imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    
    status, messages = imap.select("INBOX")
    
    # number of top emails to fetch
    N = most_recent_messages_count
        
    # total number of emails
    messages = int(messages[0])

    # see https://stackoverflow.com/a/2230571
    # see https://docs.python.org/3/library/imaplib.html#imaplib.IMAP4.search
    hasNoQuery = subject is None and fromEmail is None and toEmail is None
    messageIds = []
    criterion=[]
    if subject:
        criterion.append('SUBJECT "%s"' % subject)
        # typ, data = imap.search(None,'(SUBJECT "%s")' % subject)
        # messageIds.extend(data[0].split())
        # print('messageIds (subject)', messageIds)
    if fromEmail:
        criterion.append('FROM "%s"' % fromEmail)
        # typ, data = imap.search(None,'(FROM "%s")' % fromEmail)
        # messageIds.extend(data[0].split())
        # print('messageIds (domain)', messageIds)
    if toEmail:
        criterion.append('TO "%s"' % toEmail)
        # typ, data = imap.search(None,'(TO "%s")' % toEmail)
        # messageIds.extend(data[0].split())
        # print('messageIds (domain)', messageIds)
    if hasNoQuery:
        messageIds = [str(i) for i in range(messages, messages-N, -1)]
    else:
        typ, data = imap.search(None, f'({' '.join(criterion)})')
        messageIds.extend(data[0].split())

    msgIds, datesSent, FromEmails, files, subjects = [], [], [], [], []
    
    for i in messageIds:
        # fetch the email message by ID
        # print(f'msg id: {i}')
        # res, msg = imap.fetch(str(i), "(RFC822)")
        res, msg = imap.fetch(i, "(RFC822)")
        for response in msg:
            try:
                messageHandlerData = message_handler.messageHandler(response, OUTPUT_DIR)
                
                # print(f'messageHandlerData: {messageHandlerData}')
                
                if messageHandlerData:
                    #TODO
                    msgId, From, subject, attachmentFilepaths, dateSent = messageHandlerData['msgId'], messageHandlerData['from'], messageHandlerData['subject'], messageHandlerData['files'], messageHandlerData['date']

                    # print(f'From: {From} \n subject: {subject} \n attachmentFilepaths: {attachmentFilepaths} \n dateSent {dateSent} ')
                    
                    for filepath in attachmentFilepaths:
                        FromEmails.append(From)
                        subjects.append(subject)
                        files.append(filepath)
                        datesSent.append(dateSent)
                        msgIds.append(msgId)
            except Exception as e:
                print(f'Error: msgId: {i}. Exception: {e}')
    # close the connection and logout
    imap.close()
    imap.logout()
    return {'msgId':msgIds, 'date':datesSent, 'from': FromEmails, 'subject': subjects, 'attachments': files }