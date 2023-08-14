import pygame 
import random 
import os

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)


		img_name = 'sushi.png'
		player_img = pygame.image.load(os.path.join(img_folder, img_name)).convert()
		self.image = player_img
		
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.image.set_colorkey((0, 0, 0))

	def update(self):
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()

		go_down = True
		go_up = True
		go_left = True
		go_right = True

		

		if keystate[pygame.K_LEFT] and self.rect.left >= 0:
			self.speedx = -1
		if keystate[pygame.K_RIGHT] and self.rect.right <= WIDTH:
			self.speedx = 1
		if keystate[pygame.K_UP] and self.rect.top >= 0 and go_up:
			self.speedy = -1
		if keystate[pygame.K_DOWN] and self.rect.bottom <= HEIGHT and go_down:
			self.speedy = 1 

		self.rect.x += self.speedx
		self.rect.y += self.speedy


		if pygame.sprite.spritecollide(player, walls, False):
			
			
			self.rect.x -= self.speedx
			self.rect.y -= self.speedy
		

class Wall(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		pygame.sprite.Sprite.__init__(self)

		
		self.image = pygame.Surface((1, 50))
		self.image.fill((255,255,255))

		self.rect = self.image.get_rect()
		self.rect.center = (pos_x, pos_y)




class Figure(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((40, 100))
		self.image.fill(background_color)
		self.rect = self.image.get_rect()

		rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		pygame.draw.ellipse(self.image, rgb, (self.rect.topleft, self.rect.bottomright), 8)
		
		self.rect.center = (100, 100)
		
		self.state = False
		
		 
	def update(self):

		if event.type == pygame.MOUSEBUTTONDOWN:
			self.state = True

		elif event.type == pygame.MOUSEBUTTONUP:
			self.state = False

		if event.type == pygame.MOUSEMOTION and self.state == True:

			self.rect.move_ip(event.rel)




#параметры запуска 
WIDTH = 1920
HEIGHT = 1080
FPS = 60



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group() 


background_color = (23, 0, 0)
font = pygame.font.SysFont('couriernew', 40)

#загрузка изображения игрока 
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'sprites')


#инициализация игрока 
player = Player()
all_sprites.add(player)
figure = Figure()
all_sprites.add(figure)


#инициализация стен
walls = []
for i in range(10):
	wall = Wall(i * WIDTH // 10,0)
	all_sprites.add(wall)
	walls.append(wall)


running = True  
rgb = (0, 0, 0)
background = pygame.image.load("Maze_001.png")
background_rect = background.get_rect()

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
	all_sprites.update()

	

	#rendering
	screen.fill(background_color)
	all_sprites.draw(screen)
	screen.blit(background, background_rect)

	text = font.render(str('HELLO'), True, (123,34,1))
	screen.blit(text, (50, 50))
	pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, 60, 60))


	pygame.display.flip()
	




pygame.quit()


