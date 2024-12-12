# Thư viện
import customtkinter as ctk
from PIL import Image
from pygame import mixer
from json import load
from webbrowser import open_new

# Cửa sổ
class App():
	# Khai báo biến
	def __init__(self):
		self.size_image = (250, 150)
		self.frame_x = 0
		self.frame_y = 155
		self.frame = None
		self._frame = None
		self.format = 'utf-8-sig'
		self.i = 0
		self.type = 'intro'
		with open(r'data\screen\conversation\conversation.hocvien_data', encoding= self.format) as file:
			self.character_conversation = load(file)

	# Hàm chính
	def main(self):
		ctk.set_appearance_mode('light')
		ctk.set_default_color_theme('blue')
		# self.preplash_screen()

		self.screen = ctk.CTk()
		self.screen.title('Học viện phiêu lưu')
		self.screen.iconbitmap(r'data\screen\image\icon\app.hocvien_data')
		self.screen.geometry('800x500+400+150')
		self.screen.protocol('WM_DELETE_WINDOW', self.close)
		self.screen.rowconfigure((1), weight= 1)
		self.screen.columnconfigure((0), weight= 1)
		
		self.setup()
		self.main_screen()
		self.character_window()
		self.character_click()
		self.screen.bind('<FocusIn>', self.on_top)
		self.screen.mainloop()

	# Tắt cửa số
	def close(self):
		close_sound = mixer.Sound(r'data\screen\sound\close.hocvien_data')
		self.speak('close')
		close_sound.play()
		self.screen.after(2000, self.screen.destroy)

	# Hàm khởi tạo
	def setup(self):
		self.math_image = ctk.CTkImage(Image.open(r'data\screen\image\math\math.hocvien_data'), size= self.size_image)
		self.math_algebra_image = ctk.CTkImage(Image.open(r'data\screen\image\math\math_algebra.hocvien_data'), size= self.size_image)
		self.math_geometry_image = ctk.CTkImage(Image.open(r'data\screen\image\math\math_geometry.hocvien_data'), size= self.size_image)
		self.math_exercise_image = ctk.CTkImage(Image.open(r'data\screen\image\math\math_exercise.hocvien_data'), size= self.size_image)

		self.literature_image = ctk.CTkImage(Image.open(r'data\screen\image\literature\literature.hocvien_data'), size= self.size_image)
		self.english_image = ctk.CTkImage(Image.open(r'data\screen\image\english\english.hocvien_data'), size= self.size_image)
		self.physics_image = ctk.CTkImage(Image.open(r'data\screen\image\physics\physics.hocvien_data'), size= self.size_image)
		self.chemistry_image = ctk.CTkImage(Image.open(r'data\screen\image\chemistry\chemistry.hocvien_data'), size= self.size_image)
		self.biology_image = ctk.CTkImage(Image.open(r'data\screen\image\biology\biology.hocvien_data'), size= self.size_image)

		self.character_image = ctk.CTkImage(Image.open(r'data\screen\image\icon\character.hocvien_data'), size= (300,200))

		self.transition_sound = mixer.Sound(r'data\screen\sound\transition_sound.hocvien_data')
		self.click_sound = mixer.Sound(r'data\screen\sound\click.hocvien_data')

		self.font1 = ('roboto', 30, 'bold')
		self.font2 = ('open sans', 30)
		self.font3 = ('arial', 40, 'bold')
		self.font4 = ('arial', 20)

	# Màn hình giới thiệu
	def preplash_screen(self):
		preplash_image = ctk.CTkImage(Image.open(r'data\screen\image\icon\preplash.hocvien_data'), size= (800,500))
		preplash_sound = mixer.Sound(r'data\screen\sound\preplash.hocvien_data')
		self.fade_value = 1.0

		self.preplash = ctk.CTk()
		self.preplash.geometry('800x500+500+150')
		self.preplash.overrideredirect(True)
		ctk.CTkLabel(self.preplash, text= '', image= preplash_image).pack()
		preplash_sound.play()
		self.preplash.after(3000, self.fade)
		self.preplash.attributes('-topmost', True)
		self.preplash.mainloop()

	def fade(self):
		self.preplash.attributes('-alpha', self.fade_value)
		self.fade_value -= 0.1
		if self.fade_value <= 0:
			self.preplash.destroy()
		else:
			self.preplash.after(40, self.fade)

	# Hiệu ứng đi vào
	def _move_in(self):
		self.frame.place(x = self.frame_x, y = self.frame_y, anchor = 'center')
		self.frame_x -= 2
		if self.frame_x >= 150:
			self.screen.after(1, self._move_in)
		else:
			for i in self.screen.winfo_children():
				if str(i) == '.!ctktoplevel':
					continue
				elif str(i) != str(self.frame.winfo_parent()).replace('.!canvas',''):
					i.destroy()
			self.frame.pack(padx = 30, pady = 30, fill = 'both', expand = True)

	def move_in(self):
		self.frame_x = self.screen.winfo_screenwidth() + 10
		self.transition_sound.play()
		self._move_in()

	# Hiệu ứng đi ra
	def _move_out(self):
		self.frame.place(x = self.frame_x, y = self.frame_y, anchor = 'center')
		self.frame_x += 2
		if self.frame_x <= self.screen.winfo_screenwidth():
			self.screen.after(1, self._move_out)
		else:
			for i in self.screen.winfo_children():
				if str(i) == '.!ctktoplevel':
					continue
				elif str(i) == str(self.frame.winfo_parent()).replace('.!canvas',''):
					i.destroy()
			self._frame(False)

	def move_out(self):
		self.transition_sound.play()
		self._move_out()

	# Kiểm tra chuyển động đi vào
	def check_move(self, value, frame):
		self.frame = frame
		if value:
			self.move_in()
		else:
			self.frame_x = 150
			frame.pack(padx = 30, pady = 30, fill = 'both', expand = True)

	# Nhân vật nói chuyện
	def character_window(self):
		self.character_screen = ctk.CTkToplevel()
		self.character_screen.geometry('300x240+1400+200')
		self.character_screen.config(bg= '#abc123')
		self.character_screen.attributes('-transparentcolor', '#abc123')
		self.character_screen.attributes('-alpha', 0)
		self.character_screen.resizable(False, False)
		self.character_screen.overrideredirect(True)
		self.on_top()

		self.conversation = ctk.CTkLabel(self.character_screen, text = '', font= self.font4, 
								   text_color= '#FFFFFF', bg_color= '#abc123')
		self.conversation.pack()
		ctk.CTkButton(self.character_screen, image= self.character_image, text= '', bg_color= '#abc123',
				fg_color= '#abc123', hover_color= '#abc123', command= self._character_click).pack()
		
	def speak(self, type):
		self.type = type
		self.i = 0
		self.character_click()
		self.on_top()
		
	def character_click(self):
		self.character_screen.attributes('-alpha', 1)
		if self.i <= len(self.character_conversation[self.type]) - 1:
			text = self.character_conversation[self.type][self.i]
			text = text.split(' ')
			lis1 = []
			lis2 = []

			for num, i in enumerate(text):
				lis1.append(i)
				if (num + 1) % 6 == 0:
					lis2.append(' '.join(lis1) + '\n')
					lis1 = []
				elif num == len(text) - 1:
					lis2.append(' '.join(lis1) + '\n')
			text = ' '.join(lis2)

			self.conversation.configure(text= text)
			self.i += 1
		else:
			self.character_screen.attributes('-alpha', 0)
			self.i = 0

	def _character_click(self):
		self.click_sound.play()
		self.character_click()

	def on_top(self, object = ''):
		self.character_screen.attributes('-topmost', True)
		self.character_screen.attributes('-topmost', False)

	# Màn hình chính
	def main_screen(self, value = True):
		self.frame_main = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_main.columnconfigure((0,1,2), weight= 1)

		ctk.CTkLabel(self.screen, font= self.font1, text= 'Hạy chọn lớp:'
			   ).grid(column = 0, row = 0, padx = 160, pady = 10, sticky = 'e')
		ctk.CTkComboBox(self.screen, font= self.font1, values= ['Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', '???'], 
				  command= self.choose_class).grid(column = 0, row = 0, padx = 10, pady = 10, sticky = 'e')

		ctk.CTkButton(self.frame_main, text = 'Toán', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.math_image, hover_color= '#808b96',
				compound = 'top', command= self.math_screen
				).grid(column = 0, row = 0, pady = 10)
		
		ctk.CTkButton(self.frame_main, text = 'Ngữ văn', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.literature_image, hover_color= '#808b96',
				compound = 'top', command= self.literature_screen
				).grid(column = 1, row = 0, pady = 10)
		
		ctk.CTkButton(self.frame_main, text = 'Tiếng Anh', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.english_image, hover_color= '#808b96',
				compound = 'top', command= self.english_screen
				).grid(column = 2, row = 0, pady = 10)
		
		ctk.CTkButton(self.frame_main, text = 'Vật lý', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.physics_image, hover_color= '#808b96',
				compound = 'top', command= self.physics_screen
				).grid(column = 0, row = 1, pady = 10)
		
		ctk.CTkButton(self.frame_main, text = 'Hóa học', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.chemistry_image, hover_color= '#808b96',
				compound = 'top', command= self.chemistry_screen
				).grid(column = 1, row = 1, pady = 10)
		
		ctk.CTkButton(self.frame_main, text = 'Sinh học', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.biology_image, hover_color= '#808b96',
				compound = 'top', command= self.biology_screen
				).grid(column = 2, row = 1, pady = 10)

		self.frame_main.grid(column = 0, row = 1, padx = 30, pady = 30, sticky = 'nswe')

	def choose_class(self, class_name):
		if class_name == '???':
			open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

	# Màn hình môn Toán
	def math_screen(self, value = True):
		self.frame_math = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_math.columnconfigure((0,1,2), weight= 1)

		ctk.CTkButton(self.frame_math, text = 'Đại số', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.math_algebra_image, hover_color= '#808b96',
				compound = 'top', command= self.math_algebra_screen
				).grid(column = 0, row = 0, pady = 10)
		ctk.CTkButton(self.frame_math, text = 'Hình học', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.math_geometry_image, hover_color= '#808b96',
				compound = 'top', command= self.math_geometry_screen
				).grid(column = 1, row = 0, pady = 10)
		ctk.CTkButton(self.frame_math, text = 'Bài tập', font = self.font1, fg_color= 'transparent', 
				text_color= 'black', corner_radius = 20, image= self.math_exercise_image, hover_color= '#808b96',
				compound = 'top', command= self.math_exercise_screen
				).grid(column = 2, row = 0, pady = 10)
		ctk.CTkButton(self.frame_math, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).grid(column= 0, row= 1, columnspan = 3, pady = 10)

		self._frame = self.main_screen
		self.check_move(value, self.frame_math)
		self.speak('math_intro')

	def math_algebra_screen(self):
		with open(r'data\knowledge\math\algebra.hocvien_data', encoding= self.format) as file:
			info = file.read()
		frame_algebra = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)

		ctk.CTkLabel(frame_algebra, text= info, font= self.font2).pack(pady = 10, padx = 10)
		ctk.CTkButton(frame_algebra, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).pack(pady = 10, padx = 10)
		
		self.frame = frame_algebra
		self._frame = self.math_screen
		self.move_in()

	def math_geometry_screen(self):
		with open(r'data\knowledge\math\geometry.hocvien_data', encoding= self.format) as file:
			info = file.read()
		frame_geometry = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)

		ctk.CTkLabel(frame_geometry, text= info, font= self.font2).pack(pady = 10, padx = 10)
		ctk.CTkButton(frame_geometry, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).pack(pady = 10, padx = 10)
		
		self.frame = frame_geometry
		self._frame = self.math_screen
		self.move_in()

	def math_exercise_screen(self):
		frame_exercise = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)

		ctk.CTkButton(frame_exercise, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).pack(pady = 10, padx = 10)
		
		self.frame = frame_exercise
		self._frame = self.math_screen
		self.move_in()

	# Màn hình môn Văn
	def literature_screen(self, value = True):
		self.frame_literature = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_literature.columnconfigure((0,1,2), weight= 1)

		ctk.CTkButton(self.frame_literature, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).grid(column= 0, row= 0, columnspan = 3)

		self._frame = self.main_screen
		self.check_move(value, self.frame_literature)
		self.speak('literature_intro')

	# Màn hình môn Anh
	def english_screen(self, value = True):
		self.frame_english = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_english.columnconfigure((0,1,2), weight= 1)

		ctk.CTkButton(self.frame_english, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).grid(column= 0, row= 0, columnspan = 3)

		self._frame = self.main_screen
		self.check_move(value, self.frame_english)
		self.speak('english_intro')

	# Màn hình môn Lý
	def physics_screen(self, value = True):
		self.frame_physics = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_physics.columnconfigure((0,1,2), weight= 1)

		ctk.CTkButton(self.frame_physics, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).grid(column= 0, row= 0, columnspan = 3)

		self._frame = self.main_screen
		self.check_move(value, self.frame_physics)
		self.speak('physics_intro')

	# Màn hình môn Hóa
	def chemistry_screen(self, value = True):
		self.frame_chemistry = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_chemistry.columnconfigure((0,1,2), weight= 1)

		ctk.CTkButton(self.frame_chemistry, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).grid(column= 0, row= 0, columnspan = 3)

		self._frame = self.main_screen
		self.check_move(value, self.frame_chemistry)
		self.speak('chemistry_intro')

	# Màn hình môn Sinh
	def biology_screen(self, value = True):
		self.frame_biology = ctk.CTkScrollableFrame(self.screen, corner_radius= 20)
		self.frame_biology.columnconfigure((0,1,2), weight= 1)

		ctk.CTkButton(self.frame_biology, text= 'Trở về', font= self.font1, command= self.move_out, 
				corner_radius= 20).grid(column= 0, row= 0, columnspan = 3)

		self._frame = self.main_screen
		self.check_move(value, self.frame_biology)
		self.speak('biology_intro')

# Chạy
if __name__ == '__main__':
	mixer.init()
	app = App()
	app.main()

# pyinstaller --onefile -w --icon=app.ico --add-data "D:\Python\Lib\site-packages\customtkinter;customtkinter/" app.py