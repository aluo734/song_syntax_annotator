import tkinter.filedialog as fd
from tkinter import *
from platform import system
import os
from scipy.io import wavfile
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

class StartWindow(Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title('Syntax Labeler')
		self.geometry('500x300')
		self.config(background = '#034c52')
		if system() == 'Windows':
			self.icon = PhotoImage(master = self, file = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'logo.ico'))
			self.wm_iconphoto(True, self.icon)
		else:
			self.icon = PhotoImage(master = self, file = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'logo.png'))
			self.wm_iconphoto(True, self.icon)
		self.init_ui()
		
	def init_ui(self):
		self.browse_label = Label(self, text = 'Choose a folder of songs to label',
			background = '#017075', font = ('Arial', 30))
		self.browse_label.pack(fill = 'x', ipady = 20, pady = (0, 20))

		self.button_explore = Button(self, text = 'Browse Files', width = '10', height = '3',
			command = lambda: self.choose_folder())
		self.button_explore.pack()

		self.start_button = Button(self, text = 'Start', width = '10', height = '3',
			command = lambda: (self.make_output(), self.init_SpectroWindow()))
		self.start_button.pack(pady = 20)
		self.start_button['state'] = 'disabled'

		self.folder_label = Label(self, background = '#034c52', font = ('Arial', 18))
		self.folder_label.pack(side = 'bottom', ipady = 10, fill = 'x')

	def choose_folder(self):
		self.foldername = fd.askdirectory(parent = self, initialdir = '.', mustexist = True,
		title = 'Select folder of songs to process')
		self.files = [i for i in os.listdir(self.foldername) if i.endswith('.wav')]
		if self.foldername != '' and len(self.files) > 0:
			self.start_button['state'] = 'normal'
			self.folder_label.config(text = self.foldername.split('/')[-1] + ': ' + str(len(self.files)) + ' wav files',
				background = '#017075')
		else:
			self.folder_label.config(text = 'This folder has no wav files', background = '#017075')

	def make_output(self):
		if self.foldername != '' and len(self.files) > 0:
			self.output = open(os.path.join(self.foldername, 'syntax_annotations.txt'), 'w')
			self.output.write('song\tsyntax' + '\n')
			self.output.close()

	def init_SpectroWindow(self):
		# window
		self.spectro_window = Toplevel(self)
		self.spectro_window.title('Syntax Labeler')
		self.spectro_window.geometry('600x600')
		self.spectro_window.config(background = '#ffc0b4')
		self.spectro_window.recording = 0

		# prep spectrogram area
		self.spectro_window.song_label = Label(self.spectro_window, background = '#f48d79',
			font = ('Arial', 18))
		self.spectro_window.song_label.pack(fill = 'x', ipady = 5)
		self.spectro_window.panel = Label(self.spectro_window, background = '#ffc0b4', pady = 5)
		self.spectro_window.panel.pack()

		# close button
		self.spectro_window.button_close = Button(self.spectro_window, text = 'Close and Save',
			 width = '10', height = '2', command = self.spectro_window.destroy)
		self.spectro_window.button_close.pack(side = 'bottom', pady = (30, 5))

		# undo button
		self.spectro_window.oops = Button(self.spectro_window, text = 'oops!',
			width = '3', height = '2', command = lambda: self.undo())
		self.spectro_window.oops.pack(side = 'bottom', pady = (10, 0))
		self.spectro_window.oops.config(state = 'disabled')

		# navigation panel
		self.spectro_window.navlabel = Label(self.spectro_window, background = '#fda898')
		self.spectro_window.navlabel.pack(side = 'bottom', ipady = 10, ipadx = 20)

		self.spectro_window.navlabel.next_button = Button(self.spectro_window.navlabel, text = 'Next',
			width = '5', height = '2', command = lambda: [self.next_song(), self.spectro_image()])
		self.spectro_window.navlabel.next_button.pack(side = 'right', pady = 5, padx = (5, 50))
		self.spectro_window.navlabel.next_button.config(state = 'disabled')

		self.spectro_window.navlabel.back_button = Button(self.spectro_window.navlabel, text = 'Back',
			width = '5', height = '2', command = lambda: [self.last_song(), self.spectro_image()])
		self.spectro_window.navlabel.back_button.pack(side = 'left', pady = 5, padx = (50, 5))
		self.spectro_window.navlabel.back_button['state'] = 'disabled'

		# entry box + submit button
		self.spectro_window.submit_button = Button(self.spectro_window, text = 'Submit',
			width = '10', height = '2', command = lambda: self.add_new_row())
		self.spectro_window.submit_button.pack(side = 'bottom', pady = 5)

		self.spectro_window.entry = Entry(self.spectro_window, width = 20)
		self.spectro_window.entry.pack(side = 'bottom')

		self.spectro_window.syntax_lbl = Label(self.spectro_window, text = 'Enter syntax below',
			background = '#ffc0b4', font = ('Arial', 18))
		self.spectro_window.syntax_lbl.pack(side = 'bottom', pady = 5, ipady = 3, fill = 'x')

		# start spectrograms
		self.spectro_image()

	def next_song(self):
		self.spectro_window.recording = self.spectro_window.recording + 1
		self.spectro_window.syntax_lbl.config(text = '')
		self.spectro_window.navlabel.next_button['state'] = 'disabled'
		self.spectro_window.navlabel.back_button['state'] = 'normal'
		self.spectro_window.entry['state'] = 'normal'
		self.spectro_window.oops.config(state = 'disabled')
		if self.spectro_window.recording == 0:
			self.spectro_window.navlabel.back_button['state'] = 'disabled'

	def last_song(self):
		self.spectro_window.recording = self.spectro_window.recording - 1
		self.spectro_window.syntax_lbl.config(text = '')
		self.spectro_window.navlabel.next_button['state'] = 'disabled'
		self.spectro_window.entry['state'] = 'normal'
		self.spectro_window.oops.config(state = 'disabled')

		with open(os.path.join(self.foldername, 'syntax_annotations.txt'), 'r+') as fp:
			lines = fp.readlines()
			fp.seek(0)
			fp.truncate()
			if self.spectro_window.submit_button['state'] == 'normal':
				fp.writelines(lines[0:len(lines) - 1])
			elif self.spectro_window.submit_button['state'] == 'disabled':
				fp.writelines(lines[0:len(lines) - 2])

		if self.spectro_window.recording == 0:
			self.spectro_window.navlabel.back_button['state'] = 'disabled'

	def undo(self):
		with open(os.path.join(self.foldername, 'syntax_annotations.txt'), 'r+') as fp:
			lines = fp.readlines()
			fp.seek(0)
			fp.truncate()
			fp.writelines(lines[0:len(lines) - 1])
		self.spectro_window.syntax_lbl.config(text = '')
		self.spectro_window.submit_button['state'] = 'normal'
		self.spectro_window.entry['state'] = 'normal'
		self.spectro_window.navlabel.next_button['state'] = 'disabled'
		self.spectro_window.navlabel.back_button['state'] = 'disabled'
		self.spectro_window.oops.config(state = 'disabled')
			
	def spectro_image(self):
		self.spectro_window.song_label.config(text = self.files[self.spectro_window.recording])

		self.spectro_window.srate, self.spectro_window.sig = wavfile.read(
			os.path.join(self.foldername, self.files[self.spectro_window.recording]))
		plt.figure().set_figwidth(10)
		plt.figure().set_figheight(3)
		plt.specgram(self.spectro_window.sig, Fs = self.spectro_window.srate, NFFT = 512, noverlap = 384, pad_to = 1024)
		plt.axis('off')
		plt.margins(0, 0)
		plt.savefig('spectrogram.jpeg', bbox_inches = 'tight', pad_inches = 0)
		plt.close('all')

		self.spectro_window.img = ImageTk.PhotoImage(Image.open('spectrogram.jpeg'))
		self.spectro_window.panel.config(image = self.spectro_window.img)

		self.spectro_window.submit_button['state'] = 'normal'

	def add_new_row(self):
		self.spectro_window.syntax = list(self.spectro_window.entry.get())
		self.spectro_window.syntax_lbl.config(text = self.spectro_window.syntax)
		self.spectro_window.entry.delete(0, END)
		self.output = open(os.path.join(self.foldername, 'syntax_annotations.txt'), 'a')
		self.output.write(self.files[self.spectro_window.recording] + '\t' +
			str(self.spectro_window.syntax) + '\n')
		self.output.close()

		self.spectro_window.submit_button['state'] = 'disabled'
		self.spectro_window.entry['state'] = 'disabled'
		self.spectro_window.oops.config(state = 'normal')

		if self.spectro_window.recording < len(self.files) - 1:
			self.spectro_window.navlabel.next_button['state'] = 'normal'
		if self.spectro_window.recording == len(self.files) - 1:
			self.spectro_window.done_message = Label(self.spectro_window,
				text = 'Done! Close Window', background = '#ffc0b4', font = ('Arial', 30))
			self.spectro_window.done_message.place(relx = .5, rely = .5, anchor = 'center')

root = StartWindow()
root.mainloop()
