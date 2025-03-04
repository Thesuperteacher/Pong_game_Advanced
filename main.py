import pygame
import sys
from game.constants import *
from game.screens import StartScreen
from entities import Paddle, Ball, ScoreSystem

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

def main():
    # Game state
    game_state = "START_SCREEN"
    
    # Main game loop
    running = True
    while running:
        if game_state == "START_SCREEN":
            # Show the start screen
            start_screen = StartScreen(screen)
            result = start_screen.run()
            
            # Handle the result from the start screen
            if result == "QUIT":
                running = False
            elif result == "VS_MACHINE":
                game_state = "GAME_VS_MACHINE"
                # Initialize game objects for VS Machine mode
                initialize_game_objects(True)
            elif result == "VS_FRIEND":
                game_state = "GAME_VS_FRIEND"
                # Initialize game objects for VS Friend mode
                initialize_game_objects(False)
        
        elif game_state == "GAME_VS_MACHINE" or game_state == "GAME_VS_FRIEND":
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Power-up activation keys
                    elif event.key == pygame.K_LSHIFT:  # Left player power-up
                        left_paddle.activate_power_up()
                    elif event.key == pygame.K_RSHIFT:  # Right player power-up
                        right_paddle.activate_power_up()
            
            # Get pressed keys for paddle movement
            keys = pygame.key.get_pressed()
            
            # Left paddle movement (W/S keys)
            if keys[pygame.K_w]:
                left_paddle.move("up", SCREEN_HEIGHT)
            if keys[pygame.K_s]:
                left_paddle.move("down", SCREEN_HEIGHT)
                
            # Right paddle movement
            if game_state == "GAME_VS_FRIEND":
                # Human player (Arrow keys)
                if keys[pygame.K_UP]:
                    right_paddle.move("up", SCREEN_HEIGHT)
                if keys[pygame.K_DOWN]:
                    right_paddle.move("down", SCREEN_HEIGHT)
            else:
                # Simple AI for VS_MACHINE mode
                # Follow the ball with some delay
                if ball.y < right_paddle.rect.centery - 10:
                    right_paddle.move("up", SCREEN_HEIGHT)
                elif ball.y > right_paddle.rect.centery + 10:
                    right_paddle.move("down", SCREEN_HEIGHT)
            
            # Update ball position
            ball.update(SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Check for paddle collisions
            if ball.check_paddle_collision(left_paddle, True):
                left_paddle.increase_load(10)  # Increase load counter on hit
            
            if ball.check_paddle_collision(right_paddle, False):
                right_paddle.increase_load(10)  # Increase load counter on hit
            
            # Check for scoring
            if ball.x < 0:  # Right player scores
                score_system.update_score(2)
                ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            elif ball.x > SCREEN_WIDTH:  # Left player scores
                score_system.update_score(1)
                ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            
            # Draw everything
            screen.fill(BLACK)  # Clear the screen with black
            
            # Draw center line
            score_system.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Draw paddles and ball
            left_paddle.draw(screen)
            right_paddle.draw(screen)
            ball.draw(screen)
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

def initialize_game_objects(vs_machine):
    """Initialize game objects"""
    global left_paddle, right_paddle, ball, score_system
    
    # Create paddles
    left_paddle = Paddle(20, SCREEN_HEIGHT // 2 - 50)
    right_paddle = Paddle(SCREEN_WIDTH - 35, SCREEN_HEIGHT // 2 - 50)
    
    # Create ball at center of screen
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Create score system
    score_system = ScoreSystem()

if __name__ == "__main__":
    main() 