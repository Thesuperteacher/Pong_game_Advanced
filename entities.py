"""
Game entities for the Pong game.
This module contains the Paddle and Ball classes.
"""

import pygame
import random

class Paddle:
    """
    Paddle class for the Pong game.
    Handles paddle movement and rendering.
    """
    def __init__(self, x, y, width=15, height=100, speed=7, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color
        self.load_counter = 0  # Counter for the hit bar power-up
        self.max_load = 100    # Maximum load value
        self.is_powered_up = False  # Flag to indicate if power-up is active
        
    def move(self, direction, screen_height):
        """Move the paddle up or down within screen boundaries"""
        if direction == "up" and self.rect.top > 0:
            self.rect.y -= self.speed
        if direction == "down" and self.rect.bottom < screen_height:
            self.rect.y += self.speed
    
    def increase_load(self, amount=10):
        """Increase the load counter when hitting the ball"""
        self.load_counter = min(self.load_counter + amount, self.max_load)
        
    def activate_power_up(self):
        """Activate power-up if load counter is at maximum"""
        if self.load_counter >= self.max_load:
            self.is_powered_up = True
            self.load_counter = 0
            return True
        return False
            
    def draw(self, screen):
        """Draw the paddle on the screen"""
        # Draw the main paddle
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw the load bar below the paddle
        load_bar_height = 5
        load_bar_width = self.rect.width
        load_bar_x = self.rect.x
        load_bar_y = self.rect.bottom + 5
        
        # Background of load bar (gray)
        pygame.draw.rect(screen, (100, 100, 100), 
                         (load_bar_x, load_bar_y, load_bar_width, load_bar_height))
        
        # Filled portion of load bar (blue to red gradient based on load)
        if self.load_counter > 0:
            load_percentage = self.load_counter / self.max_load
            load_color = (int(255 * load_percentage), int(100 * (1 - load_percentage)), 255)
            pygame.draw.rect(screen, load_color, 
                            (load_bar_x, load_bar_y, 
                             int(load_bar_width * load_percentage), load_bar_height))


class Ball:
    """
    Ball class for the Pong game.
    Handles ball movement, collision detection, and rendering.
    """
    def __init__(self, x, y, radius=10, speed_x=5, speed_y=5, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.max_speed = 15  # Maximum ball speed
        
    def update(self, screen_width, screen_height):
        """Update ball position and handle wall collisions"""
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Update the rect position
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        
        # Top and bottom wall collisions
        if self.y <= self.radius or self.y >= screen_height - self.radius:
            self.speed_y *= -1
            # Add a small random variation to make gameplay more interesting
            self.speed_y += random.uniform(-0.5, 0.5)
            
    def check_paddle_collision(self, paddle, is_left_paddle):
        """
        Check for collision with a paddle and handle bounce physics
        Returns True if collision occurred
        """
        if self.rect.colliderect(paddle.rect):
            # Calculate where on the paddle the ball hit (0 to 1, from top to bottom)
            relative_intersect_y = (paddle.rect.y + paddle.rect.height/2) - self.y
            normalized_relative_intersect_y = relative_intersect_y / (paddle.rect.height/2)
            
            # Calculate bounce angle (-1 to 1) based on where the ball hit the paddle
            bounce_angle = normalized_relative_intersect_y * 0.8  # 0.8 limits the max angle
            
            # Reverse x direction and apply the bounce angle to y
            self.speed_x = -self.speed_x
            
            # Make the ball faster with each hit, up to max_speed
            speed_increase = 0.2
            if abs(self.speed_x) < self.max_speed:
                self.speed_x = self.speed_x * (1 + speed_increase)
            
            # Apply the bounce angle
            self.speed_y = -bounce_angle * abs(self.speed_x)
            
            # Move the ball outside the paddle to prevent multiple collisions
            if is_left_paddle:
                self.x = paddle.rect.right + self.radius
            else:
                self.x = paddle.rect.left - self.radius
                
            # Update the rect position
            self.rect.x = self.x - self.radius
            self.rect.y = self.y - self.radius
            
            return True
        return False
            
    def draw(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
    def reset(self, x, y):
        """Reset ball position and randomize direction"""
        self.x = x
        self.y = y
        self.rect.x = x - self.radius
        self.rect.y = y - self.radius
        
        # Reset speed but keep direction random
        self.speed_x = random.choice([-1, 1]) * 5
        self.speed_y = random.uniform(-3, 3)


class ScoreSystem:
    """
    Score system for the Pong game.
    Tracks and displays scores.
    """
    def __init__(self, font_size=36):
        self.player1_score = 0
        self.player2_score = 0
        self.font = pygame.font.Font(None, font_size)
        
    def update_score(self, player, points=1):
        """Update the score for the specified player"""
        if player == 1:
            self.player1_score += points
        else:
            self.player2_score += points
            
    def draw(self, screen, screen_width, screen_height):
        """Draw the scores on the screen"""
        # Player 1 score (left side)
        p1_text = self.font.render(str(self.player1_score), True, (255, 255, 255))
        p1_rect = p1_text.get_rect(midtop=(screen_width/4, 20))
        screen.blit(p1_text, p1_rect)
        
        # Player 2 score (right side)
        p2_text = self.font.render(str(self.player2_score), True, (255, 255, 255))
        p2_rect = p2_text.get_rect(midtop=(screen_width*3/4, 20))
        screen.blit(p2_text, p2_rect)
        
        # Draw center line
        for y in range(0, screen_height, 30):
            pygame.draw.rect(screen, (200, 200, 200), (screen_width/2 - 1, y, 2, 15)) 