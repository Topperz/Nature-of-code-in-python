import random
import matplotlib.pyplot as plt

class Perceptron:
	
	def __init__(self, n):

		self.weights = []
		self.c = 0.01

		for i in range(n):
			self.weights.append(random.uniform(-1,1))

	def activate(self, n):
		if n > 0:
			return 1
		else:
			return -1

	def feedforward(self, inputs):
		total = 0
		for i in range(len(self.weights)):
			total += inputs[i]*self.weights[i]
		return self.activate(total)

	def train(self, inputs, desired):
		guess = self.feedforward(inputs)
		error = desired - guess
		for i in range(len(self.weights)):
			self.weights[i] += self.c * error * inputs[i]

	def getWeights(self):
		return self.weights


class Trainer:

	def __init__(self, x, y, a):

		self.inputs = []

		self.inputs.append(x)
		self.inputs.append(y)
		self.inputs.append(1)
		self.answer = a


training = []

points = 200
count = 0
xmin = -400
ymin = -400
xmax = 400
ymax = 400

def f(x):
	return 0.5*x+1

# def slope():
# 	x1 = xmin
# 	y1 = f(x1)
# 	x2 = xmax
# 	y2 = f(x2)
# 	return (y2-y1)/(x2-x1)

ptron = Perceptron(3)

for i in range(points):
	x = random.uniform(xmin, xmax)
	y = random.uniform(ymin, ymax)
	answer = 1
	if y < f(x):
		answer = -1
	training.append(Trainer(x, y, answer))

	ptron.train(training[i].inputs, training[i].answer)
	weights = ptron.getWeights()
	#print weights
	x1 = xmin
	y1 = (-weights[2] - weights[0]*x1)/weights[1]
	x2 = xmax
	y2 = (-weights[2] - weights[0]*x2)/weights[1]
	#print "y1: ", x1, y1
	#print "y2: ", x2, y2
	slope1 = (y2-y1)/(x2-x1)
	#print slope1
	guess = ptron.feedforward(training[i].inputs)
	if guess > 0:
		plt.scatter(x,y, color="r" )
	else:
		plt.scatter(x,y, color="g")
	#plt.plot([x,y],[x+100, y + 10*slope1], color = "b")
	plt.plot([x1,x2],[y1,y2], color = "k")
	#print [x,y]
	#print [x+100, y + 10*slope1]
	#plt.show()
	#print weights

#print "Answer: " + str(slope())

#for i in training:
#	print i.inputs, i.answer

testing = ptron.feedforward([300,200, 1])
#plt.scatter(300,200, color = "r")
plt.axis([-400,400,-400,400])
plt.show()
print testing