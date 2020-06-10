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
		self.shop = False
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

	def move(self):
		""" перемещение точки """
		if self.status != "infected" or self.virus < 5:
			self.x += self.vx
			self.y += self.vy
			if self.x < 0 or self.x > 10 or self.x > 4.5 and self.x < 5.5:
				self.vx *= -1
				self.x += self.vx
			if self.y < 0 or self.y > 10 or self.y > 4.5 and self.y < 5.5:
				self.vy *= -1
				self.y += self.vy


	def to_shop(self):
		""" поход в магазин """
		self.x = random.random()+4.5
		self.y = random.random()+4.5

	def out_shop(self):
		""" выход из магазина """
		self.x = random.random()*10
		self.y = random.random()*10

	def infect(self, other, dst):
		""" заражение между точками """
		if self.shop and other.shop:
			if self.status == "infected" and other.status == "susceptible" and  np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst/2:
				other.status = "infected"
			elif self.status == "susceptible" and other.status == "infected" and np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst/2:
				self.status = "infected"
		else:
			if self.status == "infected" and other.status == "susceptible" and  np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst:
				other.status = "infected"
			elif self.status == "susceptible" and other.status == "infected" and np.sqrt((self.x - other.x) ** 2 + (self.y - other.y)** 2) <= dst:
				self.status = "infected" 

	def recover(self, roll, droll):
		""" лечение или смерть точки """
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
		self.people = []
		for _ in range(self.number_of_people):
			x = random.random()*10
			y = random.random()*10
			while x > 4.5 and x < 5.5 and y > 4.5 and y < 5.5:
				x = random.random()*10 
				y = random.random()*10
			person = Person(x, y, random.random()*2-1, random.random()*2-1, "susceptible")
			self.people.append(person)
		self.people[0].status = "infected"


	def number_of_infected(self, data):
		""" подсчёт количества людей с определённым статусом """
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
		""" запуск симуляции и отображение графика ситуации """
		fig, axes = plt.subplots(ncols=2, figsize=(10, 5))
		camera = Camera(fig)
		axes[0].axis("equal")
		x = []
		temp = []
		temp2 = []
		temp3 = []
		temp4 = []
		for cadr in range(self.frames):
			axes[0].plot([0, 0, 10, 10, 0],[0, 10, 10, 0, 0],"k-")
			axes[0].plot([4.5, 4.5, 5.5, 5.5, 4.5],[4.5, 5.5, 5.5, 4.5, 4.5],"y-")
			shop = []
			for _ in range(3):
				shop.append(random.choice(self.people)) 
			for i in range(self.number_of_people):
				if self.people[i] in shop:
					self.people[i].to_shop()
					self.people[i].shop = True
				else:
					if self.people[i].shop:
						self.people[i].out_shop()
						self.shop = False
					else:
						self.people[i].move()
				self.people[i].draw(axes[0])
				if self.people[i].status == "infected":
					self.people[i].virus += 1
				self.people[i].recover(self.procent_of_recover, self.procent_of_death)
				for j in range(self.number_of_people):
					self.people[i].infect(self.people[j], self.distance)

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
	covid = Simulation(100, 0.25, 0.03, 0.002, 100)
	covid.create()
	covid.run()