import pygame, random
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800,600
displayscreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Touch the cat!")

#game setting
FPS = 60
clock = pygame.time.Clock()
PLAYER_STARTING_LIVES = 7
CAT_STARTING_VELOCITY = 5
CAT_ACCELERATION      = 1

score = 0
lives = PLAYER_STARTING_LIVES
cat_velocity = CAT_STARTING_VELOCITY
cat_dx = random.choice([-1, 1])
cat_dy = random.choice([-1, 1])

font = pygame.font.Font("Franxurter.ttf", 32)

PINK = (234, 191, 218)
PURPLE = (203, 190, 218)

title_text = font.render("Touch the cat!", True, PINK)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

score_text = font.render("Score: "+str(score), True, PURPLE)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH-50, 10)

lives_text = font.render("Lives: "+str(lives), True, PURPLE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH-50, 50)

gameover_text = font.render("GAMEOVER", True, PINK)
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Click anywhere to play again!", True, PINK)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+80)

bg_image = pygame.image.load("ctc_background.png")
bg_rect  = bg_image.get_rect()
bg_rect.topleft = (0, 0)

cat_image = pygame.image.load("CatLove.png")
cat_rect  = cat_image.get_rect()
cat_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

click_sound = pygame.mixer.Sound("click_sound.wav")
miss_sound  = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("background_music.wav")


pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #if a click is made
        if event.type == pygame.MOUSEBUTTONDOWN:  #偵測滑鼠是否有點擊
            mouse_x, mouse_y = event.pos[0], event.pos[1]
            
            #滑鼠點擊到貓
            if cat_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                cat_velocity += CAT_ACCELERATION
                
                #move the cat in a new direction
                pre_cat_dx = cat_dx
                pre_cat_dy = cat_dy
                while (pre_cat_dx == cat_dx) and (pre_cat_dy == cat_dy):
                    cat_dx = random.choice([-1, 1])
                    cat_dy = random.choice([-1, 1])
                    
            else:
                miss_sound.play()
                lives -= 1
                
        
    #move the cat
    cat_rect.x += cat_dx*cat_velocity
    cat_rect.y += cat_dy*cat_velocity
    
    
    #bounce the cat off the edge of the screen
    if cat_rect.left <= 0 or cat_rect.right >= WINDOW_WIDTH:
        cat_dx = -1*cat_dx
    if cat_rect.top <= 0 or cat_rect.bottom >= WINDOW_HEIGHT:
        cat_dy = -1*cat_dy
    
    
    #update score and lives
    score_text = font.render("Score: "+str(score), True, PINK)
    lives_text = font.render("Lives: "+str(lives), True, PINK)
    
    
    #check for gameover
    if lives == 0:
        displayscreen.blit(gameover_text, gameover_rect)
        displayscreen.blit(continue_text, continue_rect)
        pygame.display.update()
        
        #pause the game until the player clicks to reset the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running   = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    lives = PLAYER_STARTING_LIVES
                    cat_rect.center = (WINDOW_HEIGHT//2, WINDOW_WIDTH//2)
                    cat_velocity = CAT_STARTING_VELOCITY
                    cat_dx = random.choice([-1, 1])
                    cat_dy = random.choice([-1, 1])
                    
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False                         
    
            
    displayscreen.blit(bg_image, bg_rect)
    displayscreen.blit(title_text, title_rect)
    displayscreen.blit(score_text, score_rect)
    displayscreen.blit(lives_text, lives_rect)
    displayscreen.blit(cat_image, cat_rect)
    
    #displayscreen.blit(gameover_text, gameover_rect)
    #displayscreen.blit(continue_text, continue_rect)
    
    pygame.display.update()
    clock.tick(FPS)
    
    
pygame.quit()