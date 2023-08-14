import numpy as np
import pygame  
import random
import sys
from os import path 

#нахождение местоположения стен на дисплее, зная их позицию на матрице
def from_matrix_to_display (matrix_position_x, matrix_position_y):
	x = (matrix_position_x + 0.25) * block_size_x
	y = (matrix_position_y + 0.25) * block_size_y
	return (x, y)

def from_display_to_matrix (center_pos):
	matrix_position_x = int(center_pos[0] / block_size_x + 0.25) 
	matrix_position_y = int(center_pos[1] / block_size_y + 0.25)
	return (matrix_position_x, matrix_position_y)


#проверка, пересекаются ли проекции прямоугольников на оси
def segment_intersection(min_x1, max_x1, min_x2, max_x2):
	return not((min_x2 >= max_x1) or (min_x1 >= max_x2))

		
#проверка на пересечение прямоугольников, которые окружают объекты
def rect_intersection(size1, center1, size2, center2):
	min_x1 = center1[0] - size1[0] / 2
	max_x1 = center1[0] + size1[0] / 2
	min_x2 = center2[0] - size2[0] / 2
	max_x2 = center2[0] + size2[0] / 2
	min_y1 = center1[1] - size1[1] / 2
	max_y1 = center1[1] + size1[1] / 2
	min_y2 = center2[1] - size2[1] / 2
	max_y2 = center2[1] + size2[1] / 2

	return segment_intersection(min_x1, max_x1, min_x2, max_x2) and segment_intersection(min_y1, max_y1, min_y2, max_y2)


def find_first_pos():
	while 1:
		y0 = random.randrange(0, matrix_height)
		x0 = random.randrange(0, matrix_width)

		if maze_map_copy[y0][x0] == 0:
			return (x0, y0)



def draw_maze(x, y, depth = 0):
	if maze_map_copy[y][x] == 1 or maze_map_copy[y][x] == 2:
		return

	maze_map_copy[y][x] = 2
	if maze_map_copy[y - 1][x] == 0:

		next_y = y - 1
		next_x = x

		#drawrect
		top_left_x = from_matrix_to_display(next_x, next_y)[0] - block_size_x / 2
		top_left_y = from_matrix_to_display(next_x, next_y)[1] - block_size_y / 2

		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(int(top_left_x), int(top_left_y), int(block_size_x) + 1, int(block_size_y * 2)))



		draw_maze(next_x, next_y, depth + 1)

	if maze_map_copy[y][x - 1] == 0:

		next_y = y
		next_x = x - 1

		#drawrect
		top_left_x = from_matrix_to_display(next_x, next_y)[0] - block_size_x / 2
		top_left_y = from_matrix_to_display(next_x, next_y)[1] - block_size_y / 2

		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(int(top_left_x), int(top_left_y), int(block_size_x * 2), int(block_size_y) + 1))


		draw_maze(next_x, next_y, depth + 1)

	if maze_map_copy[y + 1][x] == 0:

		next_y = y + 1
		next_x = x

		#drawrect
		top_left_x = from_matrix_to_display(x, y)[0] - block_size_x / 2
		top_left_y = from_matrix_to_display(x, y)[1] - block_size_y / 2

		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(int(top_left_x), int(top_left_y), int(block_size_x) + 1, int(block_size_y * 2)))


		draw_maze(next_x, next_y, depth + 1)

	if maze_map_copy[y][x + 1] == 0:

		
		next_y = y
		next_x = x + 1

		#drawrect
		top_left_x = from_matrix_to_display(x, y)[0] - block_size_x / 2
		top_left_y = from_matrix_to_display(x, y)[1] - block_size_y / 2

		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(int(top_left_x), int(top_left_y), int(block_size_x * 2), int(block_size_y) + 1))



		draw_maze(next_x, next_y, depth + 1)

	if depth == 0:
		pygame.image.save(screen, "Maze.png")


class Player(pygame.sprite.Sprite):
	def __init__(self, radius, matrix_position = None):
		pygame.sprite.Sprite.__init__(self)

		self.radius = radius
		
		is_wall = True

		if matrix_position == None:
			while is_wall:

				self.matrix_position_x = random.randint(1, matrix_width - 2)
				self.matrix_position_y = random.randint(1, matrix_height - 2)

				if maze_map[self.matrix_position_y][self.matrix_position_x] == 0:
					is_wall = False

			
		#дисплей разбивается на квадраты размером block_size * block_size. Спавн игрока происходит в центре квадрата
		pos = from_matrix_to_display(self.matrix_position_x, self.matrix_position_y)
		
		
		self.rect = pygame.Rect(pos[0] - self.radius, pos[1] - self.radius, self.radius * 2, self.radius * 2)

	def check_one_wall(self, dx, dy):  #проверка на то, пересекается ли игрок со стеной из рядом лежащих ячеек
	
		wall_position_y = self.matrix_position_y + dy
		wall_position_x = self.matrix_position_x + dx
		


		if maze_map[wall_position_y][wall_position_x] == 1:
			display_pos = from_matrix_to_display(wall_position_x, wall_position_y)
			
			if rect_intersection((self.radius * 2, self.radius * 2), self.rect.center, (block_size_x, block_size_y), (display_pos)):
				return True

		return False




	#проверка на то, возможно ли перемещение игрока в данную сторону	
	def checking(self):
		
		#проверка, не находится ли обЪект на стенах вокруг лабиринта
		if (self.matrix_position_y >= matrix_height - 1) or (self.matrix_position_x >= matrix_width - 1) or (self.matrix_position_x <= 0) or (self.matrix_position_y <= 0):
			
			return (0, 0)

		move_x = 1 #возможность перемещения игрока по оси x
		move_y = 1 #возможность перемещения игрока по оси y

		#проверка квадрата размером (block_size * 3) ** 2 на наличие квадратов - ячеек, с которыми пересекается игрок

		center = self.check_one_wall(0, 0)
		
		if center:
			return (0, 0)

		if self.speedy < 0 and self.speedx < 0: #лево верх
			left = self.check_one_wall(-1, 0)
			top = self.check_one_wall(0, -1)
			topleft = self.check_one_wall(-1, -1)

			topright = self.check_one_wall(1, -1)
			bottomleft = self.check_one_wall(-1, 1)

			if top:
				move_y = 0

			if left:
				move_x = 0

			if topleft and (not left):
				move_y = 0


			if topleft and (not top):
				move_x = 0

			if topright:
				move_y = 0

			if bottomleft:
				move_x = 0

		elif self.speedy < 0 and self.speedx > 0:  #право верх
			right = self.check_one_wall(1, 0)
			top = self.check_one_wall(0, -1)
			topright = self.check_one_wall(1, -1)

			topleft = self.check_one_wall(-1, -1)
			bottomright = self.check_one_wall(1, 1)
			if top:
				move_y = 0

			if right:
				move_x = 0

			if topright and (not right):
				move_y = 0

			if topright and (not top):
				move_x = 0

			if topleft:
				move_y = 0

			if bottomright:
				move_x = 0

		elif self.speedy > 0 and self.speedx < 0: #лево низ
			left = self.check_one_wall(-1, 0)
			bottom = self.check_one_wall(0, 1)	
			bottomleft = self.check_one_wall(-1, 1)

			topleft = self.check_one_wall(-1, -1)
			bottomright = self.check_one_wall(1, 1)
			if bottom:
				move_y = 0

			if left:
				move_x = 0

			if bottomleft and (not left):
				move_y = 0

			if bottomleft and (not bottom):
				move_x = 0

			if bottomright:
				move_y = 0

			if topleft:
				move_x = 0


		elif self.speedy > 0 and self.speedx > 0: #право низ
			right = self.check_one_wall(1, 0)			
			bottom = self.check_one_wall(0, 1)
			bottomright = self.check_one_wall(1, 1)

			topright = self.check_one_wall(1, -1)
			bottomleft = self.check_one_wall(-1, 1)


			if bottom:
				move_y = 0

			if right:
				move_x = 0

			if bottomright and (not right):
				move_y = 0

			if bottomright and (not bottom):
				move_x = 0

			if bottomleft:
				move_y = 0

			if topright:
				move_x = 0



		elif self.speedx < 0 and self.speedy == 0: #лево

			move_y = 0

			left = self.check_one_wall(-1, 0)
			topleft = self.check_one_wall(-1, -1)
			bottomleft = self.check_one_wall(-1, 1)

			if left or topleft or bottomleft: 
				move_x = 0

		elif self.speedx > 0 and self.speedy == 0: #право

			move_y = 0
			right = self.check_one_wall(1, 0)
			topright = self.check_one_wall(1, -1)
			bottomright = self.check_one_wall(1, 1)

			if right or topright or bottomright:
				move_x = 0


		elif self.speedx == 0 and self.speedy < 0: #верх
			move_x = 0

			top = self.check_one_wall(0, -1)
			topleft = self.check_one_wall(-1, -1)
			topright = self.check_one_wall(1, -1)

			if top or topleft or topright:
				move_y = 0


		elif self.speedx == 0 and self.speedy > 0: #низ

			move_x = 0
			bottom = self.check_one_wall(0, 1)
			bottomleft = self.check_one_wall(-1, 1)
			bottomright = self.check_one_wall(1, 1)

			if bottom or bottomleft or bottomright:
				move_y = 0

		
		return (move_x, move_y)


	def update(self):
		self.speedx = 0
		self.speedy = 0	

			
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx -= 1

							
		if keystate[pygame.K_UP] :
			self.speedy -= 1
					
							 
		if keystate[pygame.K_RIGHT]:
			self.speedx += 1
					
								 
		if keystate[pygame.K_DOWN]:
			self.speedy += 1
			
		
		self.rect.x += self.speedx 
		self.rect.y += self.speedy 

		

		self.matrix_position_x, self.matrix_position_y = from_display_to_matrix(self.rect.center)

		move_x, move_y = self.checking()
		
		
		self.rect.x -= self.speedx * (1 - move_x)
		self.rect.y -= self.speedy * (1 - move_y)


	def drawing(self):

		pygame.draw.circle(screen, pygame.Color('dodgerblue4'), self.rect.center, self.radius)
		
if __name__ == '__main__':
	

	FILENUMBER = (100, 3)   #(blocksize, number)
	DISP_SIZE = (1280, 720) #(width, height)

	txt_folder = path.join("saved_mazes", "txt")
	filename = f"block_size{FILENUMBER[0]}_{FILENUMBER[1]}.txt"

	filepath = path.join(txt_folder, filename)

	maze_map = np.loadtxt(filepath, dtype = int)

		

	running = True

	matrix_height = len(maze_map)
	matrix_width = len(maze_map[0])

	pygame.init()
	screen = pygame.display.set_mode(DISP_SIZE)

	FPS = 180
	clock = pygame.time.Clock()

	maze_generation = False #необходима ли генерация изображения лабиринта
	debug_mode = True #режим отладки

	if maze_generation == True:
		sys.setrecursionlimit(5000)

		maze_map_copy = np.loadtxt(filepath, dtype = int)

		#Отрисовка лабиринта
		x0, y0 = find_first_pos()
		draw_maze(x0, y0)

		background = pygame.transform.scale(pygame.image.load("Maze.png"), DISP_SIZE)

	else:

		img_folder = path.join("saved_mazes", "img")
		img_name = f"block_size{FILENUMBER[0]}_{FILENUMBER[1]}.png"
		imgpath = path.join(img_folder, img_name)

		background = pygame.transform.scale(pygame.image.load(imgpath), DISP_SIZE)


	background_rect = background.get_rect()
	
	
	
	

	#определение размеров ячейки матрицы
	block_size_y = DISP_SIZE[1] / matrix_height 
	block_size_x = DISP_SIZE[0] / matrix_width

	pygame.display.set_caption("Maze")
	

	#добавление игрока
	player = Player( min(block_size_x, block_size_y) / 4)
	
	#шрифт (для отладки)
	font = pygame.font.SysFont('couriernew', 10)


	while running:

		#input processing
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:    
					running = False
				
				
		#update
		clock.tick(FPS) 
		player.update()
		


		#rendering
		screen.fill((0, 0, 0))
		screen.blit(background, background_rect)
		player.drawing()
		

		if debug_mode:
			text1 = font.render(str(player.rect.center), True, (255, 255, 0))
			text2 = font.render(str((player.matrix_position_x, player.matrix_position_y)), True, (255, 255, 255))
			screen.blit(text1, (0, 0))
			screen.blit(text2, (0, 10))


		pygame.display.flip()


		