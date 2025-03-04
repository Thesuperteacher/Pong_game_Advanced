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

def draw_instructions(screen):
    """Draw instructions for the hold and throw feature"""
    font = pygame.font.Font(None, 24)
    
    # Instructions for the hold and throw feature
    instructions = [
        "Hold & Throw Feature:",
        "1. Fill power bar by hitting the ball",
        "2. Press SHIFT to activate power-up",
        "3. Press SPACE to hold the ball when in contact",
        "4. Rotate arrow: A/S (left paddle) or LEFT/RIGHT arrows (right paddle)",
        "5. Release SPACE to throw the ball"
    ]
    
    # Draw instructions at the bottom of the screen
    y_pos = SCREEN_HEIGHT - len(instructions) * 25 - 10
    for line in instructions:
        text = font.render(line, True, (200, 200, 200))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text, text_rect)
        y_pos += 25

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
                    # Hold ball with space key
                    elif event.key == pygame.K_SPACE:
                        # Try to hold the ball with either paddle
                        if not left_paddle.is_holding_ball and not right_paddle.is_holding_ball:
                            left_paddle.hold_ball(ball)
                            right_paddle.hold_ball(ball)
                elif event.type == pygame.KEYUP:
                    # Release the ball when space key is released
                    if event.key == pygame.K_SPACE:
                        if left_paddle.is_holding_ball:
                            left_paddle.throw_ball(ball)
                        elif right_paddle.is_holding_ball:
                            right_paddle.throw_ball(ball)
            
            # Get pressed keys for paddle movement and arrow rotation
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
            
            # Arrow rotation controls
            # Left paddle: A/S keys
            if left_paddle.is_holding_ball:
                if keys[pygame.K_a]:
                    left_paddle.rotate_arrow("counterclockwise")
                if keys[pygame.K_s]:
                    left_paddle.rotate_arrow("clockwise")
            
            # Right paddle: Left/Right arrow keys
            if right_paddle.is_holding_ball:
                if keys[pygame.K_LEFT]:
                    right_paddle.rotate_arrow("counterclockwise")
                if keys[pygame.K_RIGHT]:
                    right_paddle.rotate_arrow("clockwise")
            
            # Update ball position (only if not being held)
            if not left_paddle.is_holding_ball and not right_paddle.is_holding_ball:
                ball.update(SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                # Update ball position to follow the paddle that's holding it
                if left_paddle.is_holding_ball:
                    ball.x = left_paddle.rect.right + ball.radius
                    ball.y = left_paddle.rect.centery
                elif right_paddle.is_holding_ball:
                    ball.x = right_paddle.rect.left - ball.radius
                    ball.y = right_paddle.rect.centery
                
                # Update ball's rect
                ball.rect.x = ball.x - ball.radius
                ball.rect.y = ball.y - ball.radius
            
            # Check for paddle collisions (only if not being held)
            if not left_paddle.is_holding_ball and not right_paddle.is_holding_ball:
                if ball.check_paddle_collision(left_paddle, True):
                    left_paddle.increase_load(10)  # Increase load counter on hit
                
                if ball.check_paddle_collision(right_paddle, False):
                    right_paddle.increase_load(10)  # Increase load counter on hit
            
            # Check for scoring (only if not being held)
            if not left_paddle.is_holding_ball and not right_paddle.is_holding_ball:
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
            
            # Draw instructions
            draw_instructions(screen)
            
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