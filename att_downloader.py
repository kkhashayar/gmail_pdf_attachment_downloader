"""
Gmail attachment downloader v.1 
By: Khashayar Nariman 18, may, 2019.

Basic script description:
Checks given gimal account for PDF format attachment in given time cycle.
If file doesn't exists in current working directory will download it. 

python3-pip
sox, email, imaplib, os, sys, time, mimetypes, getpass
from socket import gethostbyname, gaierror for error handling. happenes with broken pipe.
"""

import email, imaplib, os, sys, time, mimetypes, getpass
from socket import gethostbyname, gaierror

os.system("clear")

class Att_d:
	def __init__(self):
		#self.username = "" 
		#self.password = "" 
		try:
			self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
			self.mail_folder = ""
		except gaierror:
			print("Check your connection")
		

	def connect(self):
		#self.username = input("Gmail: ")
		#self.password = getpass.getpass("Password: ")
		print()
		print("Connecting:... ")
		self.mail.login("your gmail", "yourpass")
		#self.mail_folder = "Inbox"#input("Select in mail folder: ")
		self.mail.select("inbox")
		feedback, data = self.mail.uid("search", None, "ALL")
		print("Checking for server feedback...")
		time.sleep(1)
		if feedback == "OK":
			self.inbox_item_list = data[0].split()
			print("Connected to ", self.mail_folder)

	def beep(self):
		duration = 0.1  # seconds
		freq = 800  # Hz
		os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

	def download(self):
		counter = 0
		for item in self.inbox_item_list:
			try:
				feedback, email_data = self.mail.uid("fetch", item,"(RFC822)")
				sys.stdout.flush()
			except BrokenPipeError:
				devnull = os.open(os.devnull, os.O_WRONLY)
				os.dup2(devnull, sys.stdout.fileno())
				sys.exit(1)
			counter += 1
			os.system("clear")
			print("Check pass ok ", counter)
			print()
			raw_email = email_data[0][1].decode("utf-8")
			email_message = email.message_from_string(raw_email)

			for part in email_message.walk():
				if part.get_content_maintype() == "multipart":
					continue
				if part.get("Content-Disposition") is None:
					continue
				file_name = part.get_filename()
				if type(file_name) == str:
					if file_name.endswith(".pdf"):
						print("PDF found by name: ", file_name)
						payload = part.get_payload(decode = True)
						file_path = os.path.join(os.getcwd(), file_name)
						if os.path.exists(file_path):
							print("File already exists, avoiding duplication...")
						else:
							file_path = os.path.join(os.getcwd())
							print("*************************************")
							print("Date: ",email_message["date"])
							print("From: ", email_message["from"])
							print("To: " , email_message["to"])
							print("Subject: ", email_message["subject"])
							print("*************************************")
							print()
							with open(os.path.join(file_path, file_name), "wb") as fp:
								fp.write(payload)
							self.beep()



running = True
def main():
	print("Calling block")
	gmail_downloader = Att_d()
	gmail_downloader.connect()
	gmail_downloader.download()
	print()
	print("waiting cycle..")
	time.sleep(30)
	
if __name__ == "__main__":
	while running:
		main()
