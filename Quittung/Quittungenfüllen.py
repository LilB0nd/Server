import smtplib  # Email
from xhtml2pdf import pisa
from email.mime.text import MIMEText  # email
from email.mime.multipart import MIMEMultipart  # email
from email.mime.base import MIMEBase  # email
from email import encoders  # email


class Receipt:
    def __init__(self):
        self.receipt = open("Beleg.html", "w+b")

    def converttopdf(self):
        result_file = open("Beleg.pdf", "w+b")

        # convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            "Beleg.html",  # the HTML to convert
            dest=result_file)  # file handle to recieve result

        # close output file
        result_file.close()  # close output file

        # return False on success and True on errors
        return pisa_status.err

    def closedata(self):
        self.receipt.close()


class Mail:
    def __init__(self, email_receiver):
        email_user = "triefenderkessel@gmail.com"
        pwd = "Sneaker123"
        subject = "Receipt"

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_receiver
        msg["Subject"] = subject

        body = "this is your receipt"
        msg.attach(MIMEText(body, "plain"))  # plain= type | keine html oder sonst was sondern plainer text

        filename = "Beleg.pdf"
        attachment = open(filename)

        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(email_user, pwd)

        server.sendmail(email_user, email_receiver, text)
        server.quit()


YOS = Receipt()
YOS.converttopdf()
NOS = Mail("yvo2@schule.bremen.de")
YOS.closedata()
