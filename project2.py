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
	def __init__(self, x, y, vx, vy, status):
		super().__init__(x, y, vx, vy)
		self.status = status
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
		""" перемещие точки """
		self.x += self.vx
		self.y += self.vy
		if self.x < lx or self.x > rx:
			self.vx *= -1
			self.x += self.vx
		if self.y < dy or self.y > uy:
			self.vy *= -1
			self.y += self.vy

	def go_to_carantin(self, carantin):
		""" изоляция точки от общества """
		if self.status == "infected" and self.virus >= 7 and self not in carantin:
			self.x, self.y = -3, 2
			carantin.append(self) 


	def infect(self, other, dst):
		""" заражение точки """
		if self.status == "infected" and other.status == "susceptible" and  np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst:
			other.status = "infected"
		elif self.status == "susceptible" and other.status == "infected" and np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst:
			self.status = "infected" 

	def recover(self, roll, droll):
		""" лечение или смерть точки"""
		if self.status == "infected" and random.random() < roll and self.virus > 10:
			self.status = "recovered"
		elif self.status == "infected" and random.random() > 1 - droll and self.virus > 10:
			self.status = "death"


class Simulation:
	def __init__(self, number_of_people, distance, procent_of_recover, procent_of_death, frames):
		self.number_of_people = number_of_people
		self.distance = distance
		self.procent_of_recover = procent_of_recover
		self.procent_of_death = procent_of_death
		self.frames = frames
		

	def create(self):
		""" создание общества """
		self.people = np.array([Person(random.random()*10, random.random()*10, random.random()*2-1, random.random()*2-1, "susceptible") for _ in range(self.number_of_people)])
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
		x = []
		temp = []
		temp2 = []
		temp3 = []
		temp4 = []
		carantin = []
		for cadr in range(self.frames):
			axes[0].plot([0,0,10,10,0], [0,10,10,0,0], "k-")
			axes[0].plot([-5,-5,-1,-1,-5],[0,4,4,0,0],"r-")
			for i in range(self.number_of_people):
				self.people[i].draw(axes[0])
				if self.people[i] in carantin:
					self.people[i].move(-5, -1, 0, 4)
				else:
					self.people[i].move(0, 10, 0, 10)
				if self.people[i].status == "infected":
					self.people[i].virus += 1
				self.people[i].recover(self.procent_of_recover, self.procent_of_death)
				for j in range(self.number_of_people):
					self.people[i].infect(self.people[j], self.distance)
				self.people[i].go_to_carantin(carantin)

			inf = self.number_of_infected(self.people)
			temp.append(inf[0])
			temp2.append(inf[1])
			temp3.append(inf[2])
			temp4.append(inf[3])
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
	covid = Simulation(100, 0.2, 0.03, 0.004, 100)
	covid.create()
	covid.run()