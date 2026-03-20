import os

def processInbox(
    USERNAME= os.getenv('USERNAME', 'USERNAME-REQUIRED@gmail.com'),
    APP_PASSWORD= os.getenv('APP_PASSWORD', 'APP-PASSWORD'),
    IMAP_SERVER= os.getenv('IMAP_SERVER', 'imap.gmail.com'),
    IMAP_PORT= os.getenv('IMAP_PORT', 25),

    N_COUNT= os.getenv('N_COUNT', '5'),

    FROM_EMAIL=os.getenv('FROM_EMAIL', None), # example: '<username>+<filter>@gmail.com'
    TO_EMAIL=os.getenv('TO_EMAIL', None), # example: '<username>+<filter>@gmail.com'
    OUTPUT_DIR=os.getenv('OUTPUT_DIR', './data')
):
    import os
    import pandas as pd
    from utils import connect_imap

    if OUTPUT_DIR:
        data = connect_imap.connectIMAP(USERNAME, APP_PASSWORD, IMAP_SERVER,
                                # imap_port=IMAP_PORT,
                                most_recent_messages_count=int(N_COUNT),
                                subject=None,
                                fromEmail=FROM_EMAIL,
                                toEmail=TO_EMAIL,
                                OUTPUT_DIR=OUTPUT_DIR)
        dataFrame = pd.DataFrame(data)
        dataFrame.to_csv(f'{OUTPUT_DIR}/output.csv')


def processOutbox(
    USERNAME= os.getenv('USERNAME', 'USERNAME-REQUIRED@gmail.com'),
    APP_PASSWORD= os.getenv('APP_PASSWORD', 'APP-PASSWORD'),
    SMTP_SERVER= os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    SMTP_PORT= int(os.getenv('SMTP_PORT', '587')),
    
    OUTBOX_CSV_PATH=os.getenv('OUTBOX_CSV_PATH', None),
    OUTBOX_CSV_FILE_COLUMN=os.getenv('OUTBOX_CSV_FILE_COLUMN', None),
    OUTBOX_CSV_EMAIL_COLUMN=os.getenv('OUTBOX_CSV_EMAIL_COLUMN', None),
    OUTBOX_CSV_SUBJECT_COLUMN=os.getenv('OUTBOX_CSV_SUBJECT_COLUMN', None)
):
    import pandas as pd
    from utils import sendmail
    
    if OUTBOX_CSV_PATH:
        outboxDF = pd.read_csv(OUTBOX_CSV_PATH)
        data = []
        for record in outboxDF.iloc:
            bodyFilepath = record[OUTBOX_CSV_FILE_COLUMN]
            toEmail = record[OUTBOX_CSV_EMAIL_COLUMN]
            subject = record[OUTBOX_CSV_SUBJECT_COLUMN]
            status = ''
            try:
                bodyFilepath = record[OUTBOX_CSV_FILE_COLUMN]
                toEmail = record[OUTBOX_CSV_EMAIL_COLUMN]
                subject = record[OUTBOX_CSV_SUBJECT_COLUMN]
                with open(bodyFilepath, 'r') as f:
                    bodyContent = f.read()
                    sendmail.sendmail(
                                username=USERNAME,
                                password=APP_PASSWORD,
                                smtp_server=SMTP_SERVER,
                                smtp_port=SMTP_PORT,
                                fromEmail=USERNAME,
                                toEmail=toEmail,
                                subject=subject,
                                body=bodyContent)
                    status = 'OK'
            except Exception as ex:
                status = ex
                print(f'Exception: {ex} while processing record {toEmail}, {subject}, {bodyFilepath}')
            data.append({
                    f'{OUTBOX_CSV_EMAIL_COLUMN}':toEmail,
                    f'{OUTBOX_CSV_SUBJECT_COLUMN}':subject,
                    f'{OUTBOX_CSV_FILE_COLUMN}':bodyFilepath,
                    "Status":status})
            
        dataFrame = pd.DataFrame(data)
        dataFrame.to_csv(OUTBOX_CSV_PATH)
