import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def table(img):
	msg = MIMEMultipart()
	msg['From'] = 'ali.cis22@hotmail.com'
	msg['To'] = 'ilabrahimi13@gmail.com'
	msg['Subject'] = '[URGENT] Danger !' 
	message = 'Bonjour !\n\n'+'Cette personne qui figure sur la photo en pièce jointe n est pas autorisée dans ce secteur.'+'\n\n'+'La personne est nommée : ' +str(img)+'\n\n'+'Veuillez contacter les services de sécurité à ce numéro ci-dessous !'+'\n'+'0000'
	msg.attach(MIMEText(message))
	nom_fichier = str(img)    ## Spécification du nom de la pièce jointe
	piece = open("/home/alli/Documents/"+str(img)+".jpg", "rb")    ## Ouverture du fichier
	part = MIMEBase('application', 'octet-stream')    ## Encodage de la pièce jointe en Base64
	part.set_payload((piece).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
	msg.attach(part)    ## Attache de la pièce jointe à l'objet "message"
	mailserver = smtplib.SMTP('smtp.outlook.com', 587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login('ali.cis22@hotmail.com', '************')
	mailserver.sendmail('ali.cis22@hotmail.com','ilabrahimi13@gmail.com',msg.as_string())
	mailserver.quit()


