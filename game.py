import pygame
import random
from pygame.locals import (
	K_UP, K_DOWN, K_LEFT, K_RIGHT,
	KEYDOWN, QUIT, RLEACCEL
	)

# Draw Box: draws box on specified coordinates and surface
def drawBox(x, y, color, surf):
	pygame.draw.rect(surf, color, (x+75, y+75, 24, 24))


# Score class
class Score():
	# Constructor
	def __init__(self, font):
		self.score = 0
		self.font = font
		self.score_str = self.font.render( "Score: 0", True, (255, 255, 255) )

	# Increment Score: increments socre by 1 and updates score string
	def increment_score(self):
		self.score += 1
		self.score_str = self.font.render( "Score: " + str(self.score), True, (255, 255, 255) )

	# Show Score: displays score on screen
	def show_score(self, surf):
		surf.blit(self.score_str, (75, 25) )

	# Reset: resets all variables
	def reset(self):
		self.score = 0
		self.score_str = self.font.render( "Score: 0", True, (255, 255, 255) )


# Snake class
class Snake():
	# Constructor
	def __init__(self):
		self.snk = []
		self.snk.extend([ [3,5], [2,5], [1,5] ])
		self.direction = 2
		self.eat = 0
		self.dead = 0

	# Show Snake: display game on screen
	def showSnake(self, surf):
		for i in self.snk:
			drawBox( i[0]*25, i[1]*25, (30, 59, 48), surf)

	# copy Segments: copies values of snake segments positions
	def copySegments(self):
		for i in range(len(self.snk)-1, 0, -1 ):
			self.snk[i][0] = self.snk[i-1][0]
			self.snk[i][1] = self.snk[i-1][1]

	# Move Snake: moves snake depanding upon direction and also if it has eaten any food
	def moveSnake(self):
		# if snake has eaten any food then only its head will move, so that in this way its length increases
		if self.eat == 1:
			self.eat = 0
			if self.direction == 1:
				if self.snk[0][1] > 0:
					self.snk.insert(0, [ self.snk[0][0], self.snk[0][1]-1] )
			elif self.direction == 2:
				if self.snk[0][0] < 23:
					self.snk.insert(0, [ self.snk[0][0]+1, self.snk[0][1]] )
			elif self.direction == 3:
				if self.snk[0][1] < 11:
					self.snk.insert(0, [ self.snk[0][0], self.snk[0][1]+1] )
			elif self.direction == 4:
				if self.snk[0][0] > 0:
					self.snk.insert(0, [ self.snk[0][0]-1, self.snk[0][1]] )
		# if snake has not eaten any food then only its position is updated
		else:
			if self.direction == 1:
				if self.snk[0][1] > 0:
					self.copySegments()
					self.snk[0][1] -= 1
				else:
					self.dead = 1
			elif self.direction == 2:
				if self.snk[0][0] < 23:
					self.copySegments()
					self.snk[0][0] += 1
				else:
					self.dead = 1
			elif self.direction == 3:
				if self.snk[0][1] < 11:
					self.copySegments()
					self.snk[0][1] += 1
				else:
					self.dead = 1
			elif self.direction == 4:
				if self.snk[0][0] > 0:
					self.copySegments()
					self.snk[0][0] -= 1
				else:
					self.dead = 1
		self.checkSnake()

	# Check Food: check if snake has eaten food
	def checkFood(self, food, score):
		if self.snk[0][0] == food.fx and self.snk[0][1] == food.fy:
			food.reset()
			food.list_check(self.snk)
			self.eat = 1
			score.increment_score()

	# Check Snake: check if snake has hit bite itself and is dead
	def checkSnake(self):
		for x in range(1, len(self.snk) ):
			if self.snk[0][0] == self.snk[x][0] and self.snk[0][1] == self.snk[x][1]:
				self.dead =1

	# Reset: resets all variables in class
	def reset(self):
		self.snk.clear()
		self.snk.extend([ [3,5], [2,5], [1,5] ])
		self.direction = 2
		self.eat = 0
		self.dead = 0


# Food class
class Food():
	# Constructor
	def __init__(self):
		self.fx = random.randint(0, 23)
		self.fy = random.randint(0, 11)

	# Show Food: show food on screen		
	def showFood(self, surf):
		pygame.draw.circle(surf, (194, 199, 46), (self.fx*25+75+11, self.fy*25+75+11), 12)
	
	# Reset: resets all variables in class
	def reset(self):
		self.fx = random.randint(0, 23)
		self.fy = random.randint(0, 11)

	# check if new food location is not on snake coordinates
	def list_check(self, coord_list):
		unq = 0
		while unq == 0:
			for x in range(0, len(coord_list) ):
				if self.fx == coord_list[x][0] and self.fy == coord_list[x][1]:
					unq = 0
					self.reset()
					break
				else:
					unq = 1


# game screen setting
pygame.init()
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
pygame.display.set_caption("Snake Game")

# fonts
# font is downloaded from Google Fonts. You can find its page at: https://fonts.google.com/specimen/Roboto#standard-styles
font = pygame.font.Font("Roboto-Regular.ttf", 20)
font2 = pygame.font.Font("Roboto-Regular.ttf", 40)

# grid
grid_x = 24
grid_y = 12
checkbox = 1

snake = Snake()	
food = Food()
score = Score(font)
food.list_check(snake.snk)

clock = pygame.time.Clock()
running = True
while running:
	checkbox = 0

	# checking any key pressed events
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				if snake.direction != 3:
					snake.direction = 1
			elif event.key == K_RIGHT:
				if snake.direction != 4:
					snake.direction = 2
			elif event.key == K_DOWN:
				if snake.direction != 1:
					snake.direction = 3
			elif event.key == K_LEFT:
				if snake.direction != 2:
					snake.direction = 4

	# if snake is not dead moving it
	if snake.dead == 0:
		snake.moveSnake()

	# if snake is dead then display "Game Over" and reset the game
	else:
		screen.blit( font2.render( "Game Over", True, (255, 255, 255) ), (280, 200) )
		pygame.display.flip()
		pygame.time.wait(2000)
		snake.reset()
		food.reset()
		food.list_check(snake.snk)
		score.reset()
		continue
	
	# check if snake has eaten any food
	snake.checkFood(food, score)

	# make grid on screen
	screen.fill((52, 107, 67))
	for x in range(0, grid_x, 1):
		for y in range(0, grid_y, 1):
			if checkbox:
				drawBox(x*25, y*25, (54, 191, 127), screen)
			else:
				drawBox(x*25, y*25, (45, 173, 113), screen)
			checkbox = 1 - checkbox
		checkbox = 1 - checkbox

	# diplay snake, food, score on screen
	snake.showSnake(screen)
	food.showFood(screen)
	score.show_score(screen)

	# update screen contents
	pygame.display.flip()
	clock.tick(5)
