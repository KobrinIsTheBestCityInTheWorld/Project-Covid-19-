import numpy as np
import matplotlib.pyplot as plt
import random
from celluloid import Camera

class Point:
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy


class Person(Point):
	def __init__(self, x, y, vx, vy, status, cell):
		super().__init__(x, y, vx, vy)
		self.status = status
		self.cell = cell
		self.free = True
		self.virus = 0

	def draw(self, screen):
		""" отображение точки """
		if self.status == "susceptible":
			screen.plot(self.x, self.y, "b.")
		elif self.status == "infected":
			screen.plot(self.x, self.y, "r.")
		elif self.status == "recovered":
			screen.plot(self.x, self.y, "g.")
		elif self.status == "death":
			screen.plot(self.x, self.y, "k.")

	def move(self, lx, rx, dy, uy):
		""" перемещение точки """
		self.x += self.vx
		self.y += self.vy
		if self.x < lx or self.x > rx:
			self.vx *= -1
			self.x += self.vx
		if self.y < dy or self.y > uy:
			self.vy *= -1
			self.y += self.vy

	def infect(self, other, dst):
		""" заражение точки """
		if self.cell == other.cell:
			if self.status == "infected" and other.status == "susceptible" and  np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst and random.random() < 0.7:
				other.status = "infected"
			elif self.status == "susceptible" and other.status == "infected" and np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst and random.random() < 0.7:
				self.status = "infected" 

	def recover(self, roll, droll):
		""" лечение или смерть точки """
		if self.status == "infected" and random.random() < roll and self.virus > 10:
			self.status = "recovered"
		elif self.status == "infected" and random.random() > 1 - droll and self.virus > 10:
			self.status = "death"

	def get_cell(self):
		""" определение города, в котором находится человек """
		if self.x < 10 and self.y < 10:
			return 0
		if self.x < 10 and self.y < 20:
			return 1
		if self.x < 10 and self.y < 30:
			return 2
		if self.x < 20 and self.y < 10:
			return 3		
		if self.x < 20 and self.y < 20:
			return 4
		if self.x < 20 and self.y < 30:
			return 5
		if self.x < 30 and self.y < 10:
			return 6
		if self.x < 30 and self.y < 20:
			return 7
		return 8


class Simulation:
	def __init__(self, number_of_people, distance, procent_of_recover, procent_of_death, frames):
		self.number_of_people = number_of_people
		self.distance = distance
		self.procent_of_recover = procent_of_recover
		self.procent_of_death = procent_of_death
		self.frames = frames
		

	def create(self):
		""" создание общества """
		self.people = np.array([Person(random.random()*30,random.random()*30,random.random()*2-1,random.random()*2-1,"susceptible", -1) for _ in range(self.number_of_people)])
		self.people[0].status = "infected"

	def number_of_infected(self, data):
		""" подсчёт числа точек разного статуса """
		s, i, r, d = 0, 0, 0, 0
		for elem in data:
			if elem.status == "infected":
				i += 1
			elif elem.status == "recovered":
				r += 1
			elif elem.status == "susceptible":	
				s += 1
			else:
				d += 1
		return [s, i, r, d]

	def run(self):
		""" запуск симуляции и отображение графика ситуации"""
		fig, axes = plt.subplots(ncols=2, figsize=(13, 5))
		camera = Camera(fig)
		axes[0].axis("equal")
		x = [-1]
		temp = [self.number_of_people]
		temp2 = [0]
		temp3 = [0]
		temp4 = [0]
		key = True
		for cadr in range(self.frames):
			axes[0].plot([0,0,30,30,0], [0,30,30,0,0], "k-")
			axes[0].plot([10,10], [0,30], "k-")
			axes[0].plot([20,20], [0,30], "k-")
			axes[0].plot([30,0], [10,10], "k-")
			axes[0].plot([30,0], [20,20], "k-")
			
			if temp2[-1]/self.number_of_people > 0.2 and key:
				for i in range(self.number_of_people):
					self.people[i].cell = self.people[i].get_cell()
					if random.random() > 0.5:
						self.people[i].free = False
				key = False

			for i in range(self.number_of_people):
				if self.people[i].cell == 0 and self.people[i].free == False:
					self.people[i].move(0,10,0,10)
				elif self.people[i].cell == 1 and  self.people[i].free == False:
					self.people[i].move(0,10,10,20)
				elif self.people[i].cell == 2 and self.people[i].free == False:
					self.people[i].move(0,10,20,30)
				elif self.people[i].cell == 3 and self.people[i].free == False:
					self.people[i].move(10,20,0,10)
				elif self.people[i].cell == 4 and self.people[i].free == False:
					self.people[i].move(10,20,10,20)
				elif self.people[i].cell == 5 and self.people[i].free == False:
					self.people[i].move(10,20,20,30)
				elif self.people[i].cell == 6 and self.people[i].free == False:
					self.people[i].move(20,30,0,10)
				elif self.people[i].cell == 7 and self.people[i].free == False:
					self.people[i].move(20,30,10,20)
				elif self.people[i].cell == 8 and self.people[i].free == False:
					self.people[i].move(20,30,20,30)
				else:
					self.people[i].move(0,30,0,30)

			for i in range(self.number_of_people):
				self.people[i].draw(axes[0])
				if self.people[i].status == "infected":
					self.people[i].virus += 1
				self.people[i].recover(self.procent_of_recover, self.procent_of_death)
				for j in range(self.number_of_people):
					self.people[i].infect(self.people[j], self.distance)




			info = self.number_of_infected(self.people)
			temp.append(info[0])
			temp2.append(info[1])
			temp3.append(info[2])
			temp4.append(info[3])
			x.append(cadr)
			t1, = axes[1].plot(x, temp, "b-", label="susceptible")
			t2, = axes[1].plot(x, temp2, "r-", label="infected")
			t3, = axes[1].plot(x, temp3, "g-", label="recovered")
			t4, = axes[1].plot(x, temp4, "k-", label="death")
			plt.legend(handles=[t1, t2, t3, t4])
			axes[1].set_xlabel("time")
			axes[1].set_ylabel("people")
			camera.snap()

		animation = camera.animate(repeat=False)
		plt.show()


if __name__ == '__main__':
	covid = Simulation(400, 1, 0.03, 0.004, 100)
	covid.create()
	covid.run()