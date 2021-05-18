import smtplib  # Email
from email.mime.text import MIMEText  # email
from email.mime.multipart import MIMEMultipart  # email
from email.mime.base import MIMEBase  # email
from email import encoders  # email
import pdfkit


class Receipt:

    def htmltopdf(self, url):
        """
        Wandel Quittungsseite in PDF um lol
        :param url: URL der Quittung
        """

        path_wkhtmltopdf = r"C:\Users\yvoda\OneDrive\Dokumente\GitHub\Server\Quittung\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdfkit.from_url(url, "Beleg.pdf", configuration=config)



class Mail:
    def __init__(self, email_receiver, url):
        email_user = "triefenderkessel@gmail.com"
        pwd = "Sneaker123"
        subject = "Receipt"

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_receiver
        msg["Subject"] = subject

        Receipt().htmltopdf(url)

        body = "this is your receipt"  # E-Mail text vielleicht etwas ausfürhlicher
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

# Receipt.htmltopdf("http://127.0.0.1:8000/P5/order/2/")
