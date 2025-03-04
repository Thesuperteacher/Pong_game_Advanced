import pygame
import random
import math
from game.constants import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        # Draw the button with the appropriate color
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)  # Button border
        
        # Render the text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class AnimatedBall:
    def __init__(self, x, y, radius, speed_x, speed_y, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        
    def update(self):
        # Move the ball
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off the walls
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.speed_y *= -1
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.selected_mode = None
        self.clock = pygame.time.Clock()
        
        # Create title font
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 28)
        
        # Create buttons
        button_width = 250
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.vs_machine_button = Button(
            button_x, 
            SCREEN_HEIGHT // 2, 
            button_width, 
            button_height, 
            "Play vs Machine", 
            (100, 100, 200),  # Blue
            (130, 130, 230)   # Light blue (hover)
        )
        
        self.vs_friend_button = Button(
            button_x, 
            SCREEN_HEIGHT // 2 + button_height + 20, 
            button_width, 
            button_height, 
            "Play vs Friend", 
            (200, 100, 100),  # Red
            (230, 130, 130)   # Light red (hover)
        )
        
        # Create animated balls for the background
        self.balls = []
        for _ in range(5):
            radius = random.randint(5, 15)
            x = random.randint(radius, SCREEN_WIDTH - radius)
            y = random.randint(radius, SCREEN_HEIGHT - radius)
            speed_x = random.uniform(-3, 3)
            speed_y = random.uniform(-3, 3)
            
            # Ensure the ball is moving
            if abs(speed_x) < 1:
                speed_x = 1 if speed_x >= 0 else -1
            if abs(speed_y) < 1:
                speed_y = 1 if speed_y >= 0 else -1
                
            color = (
                random.randint(150, 255),
                random.randint(150, 255),
                random.randint(150, 255)
            )
            
            self.balls.append(AnimatedBall(x, y, radius, speed_x, speed_y, color))
        
        # Animation variables
        self.title_bounce = 0
        self.title_bounce_dir = 1
        self.title_bounce_speed = 0.5
        self.title_bounce_max = 10
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return "QUIT"
            
            # Mouse events
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            
            # Check button hover states
            self.vs_machine_button.check_hover(mouse_pos)
            self.vs_friend_button.check_hover(mouse_pos)
            
            # Check button clicks
            if mouse_clicked:
                if self.vs_machine_button.is_clicked(mouse_pos, True):
                    self.running = False
                    return "VS_MACHINE"
                
                if self.vs_friend_button.is_clicked(mouse_pos, True):
                    self.running = False
                    return "VS_FRIEND"
        
        return None
    
    def update(self):
        # Update animated balls
        for ball in self.balls:
            ball.update()
            
        # Update title bounce animation
        self.title_bounce += self.title_bounce_speed * self.title_bounce_dir
        if abs(self.title_bounce) >= self.title_bounce_max:
            self.title_bounce_dir *= -1
    
    def draw(self):
        # Fill the background
        self.screen.fill(BLACK)
        
        # Draw animated balls
        for ball in self.balls:
            ball.draw(self.screen)
        
        # Draw paddles (decorative)
        paddle_height = 80
        paddle_width = 10
        pygame.draw.rect(self.screen, WHITE, 
                         (20, SCREEN_HEIGHT // 2 - paddle_height // 2, 
                          paddle_width, paddle_height))
        pygame.draw.rect(self.screen, WHITE, 
                         (SCREEN_WIDTH - 20 - paddle_width, 
                          SCREEN_HEIGHT // 2 - paddle_height // 2, 
                          paddle_width, paddle_height))
        
        # Draw title with bounce effect
        title_y_offset = math.sin(self.title_bounce * 0.1) * 5
        title_surface = self.title_font.render("PONG GAME", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + title_y_offset))
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = self.subtitle_font.render("Select Game Mode", True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw buttons
        self.vs_machine_button.draw(self.screen)
        self.vs_friend_button.draw(self.screen)
        
        # Draw instructions at the bottom
        instructions = self.subtitle_font.render("Press ESC to quit", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
        
    def run(self):
        while self.running:
            # Handle events
            result = self.handle_events()
            if result:
                return result
            
            # Update animations
            self.update()
                
            # Draw everything
            self.draw()
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(FPS)
            
        return self.selected_mode 