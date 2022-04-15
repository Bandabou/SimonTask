from tkinter import *
import random

import time

#todo:
# when calculating average congruent time and dividing by zero, error is given

class simon_task_gui():
	def __init__(self, root):
		self.__window = root
		self.__window.title('Simon Task (GUI)')
		self.__window.maxsize(1200,800)     
		
		 
		self.__toolbar = Frame(self.__window)

		self.__nr_stimuli = Label(self.__toolbar)
		self.__nr_stimuli.config(text = 'nr stimuli')
		self.__nr_stimuli.config(font = 'Arial 20 bold')
		self.__nr_stimuli.pack(side = 'left')
		self.__nr_stimuli_entry = Entry(self.__toolbar)        
		self.__nr_stimuli_entry.config(width = 5)
		self.__nr_stimuli_entry.config(font = 'Arial 20 bold')
		self.__nr_stimuli_entry.pack(side = 'left')

		self.__ms_between = Label(self.__toolbar)
		self.__ms_between.config(text = 'ms between')
		self.__ms_between.config(font = 'Arial 20 bold')
		self.__ms_between.pack(side = 'left')
		
		self.__ms_between_entry = Entry(self.__toolbar)
		self.__ms_between_entry.config(width = 5)
		self.__ms_between_entry.config(font = 'Arial 20 bold')
		self.__ms_between_entry.pack(side = 'left')
	 

		self.__ms_visible = Label(self.__toolbar)
		self.__ms_visible.config(text = 'ms visible')
		self.__ms_visible.config(font = 'Arial 20 bold')
		self.__ms_visible.pack(side = 'left')
		self.__ms_visible_entry = Entry(self.__toolbar)
		self.__ms_visible_entry.config(width = 5)
		self.__ms_visible_entry.config(font = 'Arial 20 bold')
		self.__ms_visible_entry.pack(side = 'left')

		self.__btn_New_Task = Button(self.__toolbar)
		self.__btn_New_Task.config(text = 'Start New Simon Task')
		self.__btn_New_Task.config(font = 'Arial 20 bold')
		self.__btn_New_Task.pack(side = 'left')
		self.__btn_New_Task.config(command =self.__simon_task_start)

		self.__btn_cancel = Button(self.__toolbar)
		self.__btn_cancel.config(text = 'Cancel')
		self.__btn_cancel.config(font = 'Arial 20 bold')		
		self.__btn_cancel.pack(side = 'left')
		self.__btn_cancel.config(command = self.__simon_task_cancel)
		

		self.__btn_help = Button(self.__toolbar)
		self.__btn_help.config(text = 'Help')
		self.__btn_help.config(font = 'Arial 20 bold')
		self.__btn_help.pack(side = 'left')
		self.__btn_help.config(command = self.__display_help)

		self.__toolbar.pack(side = 'bottom')

	   
		
		#create canvas
		
		self.__canvas = Canvas(self.__window)
		self.__canvas.config(width = 1200)
		self.__canvas.config(height = 800)
		self.__canvas.config(background = 'white')
		self.__canvas.pack()

		#bind the keys
	   
		self.__canvas.bind("<Key>" , self.__keypress)        
	   

		
		#helper list to convert number to corresponding square description		
		self.__rect_list = [ None,['red','right'],['red','left'],['blue','left'],['blue','right'] ]

		
		
		 
	def __display_help(self):
		self.__canvas.delete('all')		
		self.__canvas.create_text(100 , 100 , text = 'welcome to the Simon Task', font = 'arial 20 bold', anchor = 'nw')        
		self.__canvas.create_text(100 , 150 , text = 'Blue square: press the "q" key', font = 'arial 20 bold', anchor = 'nw')
		self.__canvas.create_text(100 , 200 , text = 'Red square: press the "p" key', font = 'arial 20 bold', anchor = 'nw')
		self.__canvas.create_text(100 , 250 , text = 'Press the start button to start task', font = 'arial 20 bold', anchor = 'nw')
		

	
	

	
		
	
	def __simon_task_start(self):
		self.__congruent_times = []
		self.__incongruent_times = []
		self.__nr_drawn  = 0
		self.__canvas.delete('all') 
		try:
			self.__nrStimuli = int(self.__nr_stimuli_entry.get())
			self.__msBetween = int(self.__ms_between_entry.get())        
			self.__msVisible = int(self.__ms_visible_entry.get())
			
			self.__canvas.focus_set()
		
			self.__simon_task_draw()

		except ValueError:
			self.__canvas.create_text(100 , 100 ,text = 'Enter valid values please' , font = 'arial 20 bold' , anchor = 'nw')


		
		   
					 
		

	def __simon_task_draw(self):

		

		self.__canvas.focus_set()

		if self.__nrStimuli > self.__nr_drawn:  
			
			self.__rect_choice = random.randint(1, 4)
			

			if self.__rect_choice == 1  :
				self.__canvas.create_rectangle(1000 , 200 , 1150 , 350 , fill = 'red' , tags = 'rc') #congruent
				self.__start = time.perf_counter()
				
			elif self.__rect_choice == 2 :
				
				self.__canvas.create_rectangle(50 , 200 , 200 , 350 , fill = 'red' , tags = 'ri') #incongruent
				self.__start = time.perf_counter()
				
				
			elif self.__rect_choice == 3 :
				self.__canvas.create_rectangle(50 , 200 , 200 , 350 , fill = 'blue' , tags = 'bc') #congruent
				self.__start = time.perf_counter()
			  
	 
			elif self.__rect_choice == 4 :
				self.__canvas.create_rectangle(1000 , 200 , 1150 , 350 , fill = 'blue' , tags = 'bi') #incongruent
				self.__start = time.perf_counter()
				

		
			self.__nr_drawn += 1
			print(self.__nr_drawn)
			
			self.__loopback = self.__canvas.after(self.__msVisible , self.__simon_task_loopback)


		else: 

			#completed test                       
			self.__window.focus_set()
			self.__canvas.create_text(100 , 100 , text= 'you have completed the simon task for ' + str(self.__nrStimuli) +
				' stimuli. Great!' , font = 'arial 20 bold' , anchor = 'nw')        
			
			correct_amount = (len(self.__congruent_times) + len(self.__incongruent_times))


			self.__canvas.create_text(100 , 150 , text= str(correct_amount)+ ' keys were correct.' , font = 'arial 20 bold' , anchor = 'nw')

			#calculating the average
			try:
				avg_congruent = int(round(  sum(self.__congruent_times)*1000 )/  float(len(self.__congruent_times)))
				avg_incongruent = int(round(sum(self.__incongruent_times)*1000)/  float(len(self.__incongruent_times)))
				
				self.__canvas.create_text(100 , 200 , text= 'congruent reaction time: ' + str(avg_congruent) + ' ms (average over ' +
				 	str(len(self.__congruent_times)) + ' stimuli)' , font = 'arial 20 bold' , anchor = 'nw')
				
				self.__canvas.create_text(100 , 250 , text= 'incongruent reaction time: ' + str(avg_incongruent) + 'ms (average over ' + 
					str(len(self.__incongruent_times)) + ' stimuli)' , font = 'arial 20 bold' , anchor = 'nw')
						
			except ZeroDivisionError:
				self.__canvas.create_text(100 , 200 , text= 'to get better results, try using more stimuli' , font = 'arial 20 bold' , anchor = 'nw')

				


	#delay amount ms between the squares for the draw functions			
	def __simon_task_loopback(self):
		self.__canvas.delete('all')
		self.__window.focus_set()
		self.__draw_process = self.__canvas.after(self.__msBetween , self.__simon_task_draw)


	def __simon_task_cancel(self):
		self.__canvas.delete('all')
		
		self.__window.focus_set()
		self.__canvas.create_text(100 , 100 , text = 'you canceled the Simon Task' , font = 'arial 20 bold' , anchor = 'nw')
		try:
			self.__canvas.after_cancel(self.__draw_process)
			self.__canvas.after_cancel(self.__loopback)
		except AttributeError:
			pass 			 
		
		
	def __keypress(self, event):		
			self.__window.focus_set()	
			self.__finish = time.perf_counter() 
			reaction_time = self.__finish - self.__start			

			correct = False
			congruent = False

			if event.keysym == 'p':
				if self.__rect_choice <= 2:
					correct = True
				if self.__rect_choice == 1:
					congruent = True

			if event.keysym == 'q':
				if self.__rect_choice >= 3:
					correct = True
				if self.__rect_choice == 3:
					congruent = True

			if correct:
				self.__canvas.delete('all')		
				
				if congruent:
					self.__congruent_times.append(reaction_time)
					message = 'congruent'
				else:
					self.__incongruent_times.append(reaction_time)
					message = 'incongruent'
			else:
				message = 'incorrect'


			print('detected response \''+ event.keysym + '\' to stimulus ' + str(self.__rect_list[self.__rect_choice]) + 
				' , reaction time = ' + str(int(round(reaction_time*1000))) + ' ms, response was ' + message)

					   
			
	 
	   


def main():
	root = Tk()
	Simon_Task = simon_task_gui(root)
	root.mainloop()

main()
