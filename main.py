import pygame
import sys
from game.constants import *
from game.screens import StartScreen

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
                print("Starting game vs machine...")
                # We'll implement this mode later
                running = False  # Temporary until we implement the game
            elif result == "VS_FRIEND":
                game_state = "GAME_VS_FRIEND"
                print("Starting game vs friend...")
                # We'll implement this mode later
                running = False  # Temporary until we implement the game
        
        elif game_state == "GAME_VS_MACHINE" or game_state == "GAME_VS_FRIEND":
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update game objects
            # (We'll add this later)
            
            # Draw everything
            screen.fill(BLACK)  # Clear the screen with black
            
            # Draw game objects
            # (We'll add this later)
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 