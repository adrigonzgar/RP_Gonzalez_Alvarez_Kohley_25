import pygame
import sys
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, GREEN, BLUE
from Welcome_Screen import welcome_screen
from player import Player
from game_manager import GameManager, DemoPlayer
from game_over import show_game_over_screen
from victory_screen import show_victory_screen
from loading_screen import show_loading_screen
from sound_manager import SoundManager
from particle_system import ParticleSystem
from highscore_manager import HighScoreManager
from name_entry_screen import show_name_entry_screen
from camera_shake import CameraShake

def show_level_selector(screen, clock):
    """
    Shows a level selector for testing
    
    Returns:
        int: Selected level number (1-5)
    """
    selected_level = 1
    max_level = 5
    
    # Fonts
    font_large = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    # Colors
    SELECTOR_BG = (30, 30, 30)
    SELECTOR_BORDER = (100, 100, 100)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected_level = max(1, selected_level - 1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected_level = min(max_level, selected_level + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return selected_level
                elif event.key == pygame.K_ESCAPE:
                    return 1  # Return to level 1 by default
        
        # Draw background
        screen.fill(BLACK)
        
        # Title
        title_text = font_large.render("SELECT LEVEL", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Draw levels
        level_spacing = 120
        start_x = (SCREEN_WIDTH - (max_level * level_spacing)) // 2 + 60
        
        for level in range(1, max_level + 1):
            x = start_x + (level - 1) * level_spacing
            y = SCREEN_HEIGHT // 2
            
            # Draw level box
            box_size = 80
            box_rect = pygame.Rect(x - box_size//2, y - box_size//2, box_size, box_size)
            
            if level == selected_level:
                # Selected level - highlighted
                pygame.draw.rect(screen, YELLOW, box_rect)
                pygame.draw.rect(screen, WHITE, box_rect, 4)
                level_color = BLACK
            else:
                # Unselected level
                pygame.draw.rect(screen, SELECTOR_BG, box_rect)
                pygame.draw.rect(screen, SELECTOR_BORDER, box_rect, 2)
                level_color = WHITE
            
            # Level number
            level_text = font_large.render(str(level), True, level_color)
            level_text_rect = level_text.get_rect(center=(x, y))
            screen.blit(level_text, level_text_rect)
            
            # Level name below
            level_names = ["Tutorial", "Speed Up", "Moving", "Vertical", "Gauntlet"]
            name_text = font_small.render(level_names[level - 1], True, WHITE if level != selected_level else YELLOW)
            name_rect = name_text.get_rect(center=(x, y + 60))
            screen.blit(name_text, name_rect)
        
        # Instructions
        instructions = font_small.render("Use ← → to select, ENTER to start, ESC to cancel", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        screen.blit(instructions, instructions_rect)
        
        # Arrow indicators
        if selected_level > 1:
            left_arrow = font_large.render("◄", True, YELLOW)
            screen.blit(left_arrow, (start_x - 100, SCREEN_HEIGHT // 2 - 30))
        
        if selected_level < max_level:
            right_arrow = font_large.render("►", True, YELLOW)
            screen.blit(right_arrow, (start_x + (max_level - 1) * level_spacing + 80, SCREEN_HEIGHT // 2 - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

def show_level_complete_message(screen, clock, next_level):
    """
    Shows a blinking level completed message
    
    Args:
        screen: Pygame surface
        clock: Pygame clock
        next_level: Next level number
    """
    # Message duration (2 seconds)
    duration = 2.0
    start_time = time.time()
    
    # Save current screen content
    screen_copy = screen.copy()
    
    # Fonts
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    
    while time.time() - start_time < duration:
        # Calculate blink
        elapsed = time.time() - start_time
        blink = int(elapsed * 8) % 2  # Blinks 8 times per second
        
        # Restore original screen
        screen.blit(screen_copy, (0, 0))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        # Draw message if in visible phase of blink
        if blink == 1:
            # Main text
            level_text = font_large.render(f"LEVEL {next_level}", True, YELLOW)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            
            # Text shadow
            shadow_text = font_large.render(f"LEVEL {next_level}", True, (50, 50, 0))
            shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 27))
            screen.blit(shadow_text, shadow_rect)
            screen.blit(level_text, level_rect)
            
            # Secondary text
            complete_text = font_medium.render("LEVEL COMPLETE!", True, WHITE)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(complete_text, complete_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Process events to prevent program freeze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_game_loop(screen, clock, is_fullscreen, sound_manager, highscore_manager, starting_level=1):
    """Main game loop for Donkey Kong"""
    running = True
    game_start_time = time.time()
    current_screen = screen
    current_fullscreen = is_fullscreen
    
    # Create virtual surface to render the game
    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create player (Mario) - Starts at center, falling from above
    player = Player(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    player.sound_manager = sound_manager  # Assign sound manager to player
    
    # Create game manager
    game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_manager.sound_manager = sound_manager  # Assign sound manager
    
    # Create particle system
    particle_system = ParticleSystem()
    game_manager.particle_system = particle_system  # Assign to game manager
    
    # Create camera shake system
    camera_shake = CameraShake()
    
    # Set initial level
    game_manager.level = starting_level
    game_manager.initialize_level()
    
    # Play level music
    if sound_manager:
        sound_manager.play_music("level")
    
    # Variables to detect events
    previous_lives = player.lives
    
    # Game variables
    dt = clock.get_time() / 1000.0  # Delta time in seconds
    
    while running:
        dt = clock.get_time() / 1000.0
        
        # Get pressed keys
        keys_pressed = pygame.key.get_pressed()
        
        # Update player
        player.update(keys_pressed, game_manager.get_platforms(), game_manager.get_ladders(), dt, game_manager.get_moving_platforms())
        
        # Detect life loss for camera shake
        if player.lives < previous_lives:
            camera_shake.start_shake(intensity=15, duration=20)
        previous_lives = player.lives
        
        # Update game logic
        level_completed = game_manager.update(player)
        
        # Update particle system
        particle_system.update()
        
        # Update camera shake
        camera_shake.update()
        
        # Check if level was completed
        if level_completed:
            # Check if level 5 was completed (last level)
            if game_manager.level >= 5:
                # Calculate total play time
                total_time = time.time() - game_start_time
                
                # Get final statistics
                player_stats = player.get_stats()
                game_manager_stats = {
                    'score': game_manager.get_score(),
                    'level': game_manager.level,
                    'barrels_dodged': getattr(game_manager, 'barrels_dodged', 0),
                    'powerups_collected': getattr(game_manager, 'powerups_collected', 0)
                }
                
                # Play victory sound
                if sound_manager:
                    sound_manager.play_sound('victory')
                
                # Show victory screen
                show_victory_screen(screen, clock, player_stats, game_manager_stats, total_time)
                
                # Return to main menu
                return
            else:
                # Play level complete sound
                if sound_manager:
                    sound_manager.play_sound('level_complete')
                
                # Show level complete message
                show_level_complete_message(screen, clock, game_manager.level + 1)
                
                # Advance to next level
                game_manager.level += 1
                game_manager.initialize_level()
                
                # Reset player position - falling from center
                player.reset_position(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2)
        
        # Check Game Over
        if player.lives <= 0:
            # Calculate total play time
            total_time = time.time() - game_start_time
            
            # Get statistics
            player_stats = player.get_stats()
            game_manager_stats = {
                'score': game_manager.get_score(),
                'level': game_manager.level,
                'barrels_dodged': getattr(game_manager, 'barrels_dodged', 0),
                'powerups_collected': getattr(game_manager, 'powerups_collected', 0)
            }
            
            # Check if it's a high score
            total_score = player_stats['score'] + game_manager_stats['score']
            if highscore_manager.is_highscore(total_score):
                # Ask player for name
                rank = highscore_manager.get_rank(total_score)
                player_name = show_name_entry_screen(screen, clock, total_score, rank)
                highscore_manager.add_highscore(player_name, total_score, game_manager.level)
            
            # Show Game Over screen
            choice = show_game_over_screen(screen, clock, player_stats, game_manager_stats, total_time)
            
            if choice == 0:  # Return to start
                return  # Exit loop to return to main menu
            elif choice == 2:  # Exit game
                pygame.quit()
                sys.exit()
            # If choice == 1 (statistics), already handled in function
        
        # Draw everything on virtual surface
        game_surface.fill(BLACK)
        
        # Draw map and all its elements
        game_manager.draw(game_surface)
        
        # Draw player
        player.draw(game_surface)
        
        # Draw particles (on top of player)
        particle_system.draw(game_surface)
        
        # Game UI
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Player statistics
        stats = player.get_stats()
        total_score = stats['score'] + game_manager.get_score()
        
        score_text = font_small.render(f"Score: {total_score}", True, WHITE)
        level_text = font_small.render(f"Level: {game_manager.level}", True, WHITE)
        
        game_surface.blit(score_text, (20, 20))
        # Draw hearts instead of lives text
        game_manager.draw_hearts(game_surface, stats['lives'], 20, 50)
        game_surface.blit(level_text, (20, 80))
        
        # Show number of active barrels
        barrel_count = len(game_manager.barrels)
        barrel_text = font_tiny.render(f"Barrels: {barrel_count}", True, RED)
        game_surface.blit(barrel_text, (20, 110))
        
        # Controls
        controls_text = font_tiny.render("WASD/Arrows, Space=jump, ESC=exit, R=menu, F11=fullscreen, L=level select", True, WHITE)
        game_surface.blit(controls_text, (10, SCREEN_HEIGHT - 30))
        
        # Elapsed time
        elapsed = time.time() - game_start_time
        time_text = font_tiny.render(f"Game Time: {elapsed:.1f}s", True, GREEN)
        game_surface.blit(time_text, (SCREEN_WIDTH - 150, 20))
        
        
        # Get camera shake offset
        shake_x, shake_y = camera_shake.get_offset()
        
        # Scale and draw on real screen (works in both fullscreen and maximized window)
        screen_w, screen_h = current_screen.get_size()
        
        # If window is larger than original size, scale
        if screen_w != SCREEN_WIDTH or screen_h != SCREEN_HEIGHT:
            # Calculate scale to maintain aspect ratio
            scale_x = screen_w / SCREEN_WIDTH
            scale_y = screen_h / SCREEN_HEIGHT
            scale = min(scale_x, scale_y)
            
            new_w = int(SCREEN_WIDTH * scale)
            new_h = int(SCREEN_HEIGHT * scale)
            
            scaled_surface = pygame.transform.scale(game_surface, (new_w, new_h))
            
            # Center on screen with shake
            x = (screen_w - new_w) // 2 + int(shake_x * scale)
            y = (screen_h - new_h) // 2 + int(shake_y * scale)
            
            current_screen.fill(BLACK)
            current_screen.blit(scaled_surface, (x, y))
        else:
            # Original size, no scaling
            current_screen.blit(game_surface, (shake_x, shake_y))
        
        pygame.display.flip()
        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update window size (content is automatically scaled)
                if not current_fullscreen:
                    current_screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    current_screen, current_fullscreen = toggle_fullscreen(current_screen, current_fullscreen)
                elif event.key == pygame.K_r:
                    # Return to welcome screen
                    welcome_screen(screen, clock)
                    game_start_time = time.time()  # Reset counter
                elif event.key == pygame.K_SPACE:
                    # Additional jump with spacebar
                    player.jump()

def demo_game_loop(screen, clock):
    """Game loop in demo mode (automatic)"""
    # Create player (Mario) - Starts at center, falling from above
    player = Player(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Create game manager
    game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Create automatic player for demo
    demo_player = DemoPlayer(player, game_manager.get_platforms(), game_manager.get_ladders(), game_manager)
    
    # Game variables
    dt = clock.get_time() / 1000.0
    demo_duration = 60.0  # 60 seconds of demo
    demo_start_time = time.time()
    
    while True:
        dt = clock.get_time() / 1000.0
        elapsed_demo_time = time.time() - demo_start_time
        
        # End demo after time limit
        if elapsed_demo_time >= demo_duration:
            return
        
        # Get automatic input from demo
        demo_keys = demo_player.update()
        
        # Update player with automatic input
        player.update(demo_keys, game_manager.get_platforms(), game_manager.get_ladders(), dt, game_manager.get_moving_platforms())
        
        # Update game logic
        game_manager.update(player)
        
        # If player dies in demo, restart
        if player.lives <= 0:
            player = Player(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
            demo_player = DemoPlayer(player, game_manager.get_platforms(), game_manager.get_ladders(), game_manager)
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw map and all its elements
        game_manager.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Demo UI
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # DEMO indicator
        demo_text = font_large.render("DEMO", True, RED)
        screen.blit(demo_text, (20, 20))
        
        # Basic statistics
        stats = player.get_stats()
        total_score = stats['score'] + game_manager.get_score()
        
        score_text = font_small.render(f"Score: {total_score}", True, WHITE)
        level_text = font_small.render(f"Level: {game_manager.level}", True, WHITE)
        
        screen.blit(score_text, (20, 60))
        # Draw hearts instead of lives text
        game_manager.draw_hearts(screen, stats['lives'], 20, 90)
        screen.blit(level_text, (20, 120))
        
        # Demo time remaining
        time_left = demo_duration - elapsed_demo_time
        time_text = font_tiny.render(f"Demo ends in: {time_left:.1f}s", True, YELLOW)
        screen.blit(time_text, (SCREEN_WIDTH - 250, 20))
        
        # Exit instruction
        exit_text = font_tiny.render("Press any key to play", True, GREEN)
        screen.blit(exit_text, (SCREEN_WIDTH//2 - exit_text.get_width()//2, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

        # Events - any key ends the demo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    return  # End demo and return to menu

def toggle_fullscreen(screen, is_fullscreen):
    """
    Toggles between maximized window and normal window mode (keeps title bar)
    
    Args:
        screen: Current pygame surface
        is_fullscreen: Current fullscreen state
        
    Returns:
        tuple: (new_screen, new_fullscreen_state)
    """
    if is_fullscreen:
        # Switch to normal window mode
        new_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    else:
        # Switch to maximized window (keeps title bar)
        # Get screen information
        info = pygame.display.Info()
        # Create window of screen size but with title bar
        new_screen = pygame.display.set_mode((info.current_w, info.current_h - 70), pygame.RESIZABLE)
    
    pygame.display.set_caption("Donkey Kong")
    return new_screen, not is_fullscreen

def main():
    """Main program function"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Donkey Kong")
    clock = pygame.time.Clock()
    is_fullscreen = False  # Fullscreen state
    
    # Sound system disabled
    sound_manager = None
    
    # Create high score manager
    highscore_manager = HighScoreManager()
    
    # Show loading screen at startup
    initialization_steps = [
        (lambda: pygame.font.init(), "Loading fonts"),
        (lambda: time.sleep(0.2), "Loading game resources"),
        (lambda: time.sleep(0.2), "Loading level configurations"),
        (lambda: time.sleep(0.2), "Preparing game engine"),
        (lambda: time.sleep(0.2), "Loading sprites and graphics"),
        (lambda: time.sleep(0.2), "Setting up game world"),
        (lambda: time.sleep(0.1), "Finalizing initialization"),
    ]
    
    show_loading_screen(screen, clock, initialization_steps)
    
    # Main program loop
    while True:
        # Show welcome screen
        mode = welcome_screen(screen, clock)
        
        if mode == "demo":
            # Start demo mode
            demo_game_loop(screen, clock)
        elif mode == "level_select":
            # Show level selector
            selected_level = show_level_selector(screen, clock)
            # Start game at selected level
            main_game_loop(screen, clock, is_fullscreen, sound_manager, highscore_manager, selected_level)
        else:
            # Start main game from level 1
            main_game_loop(screen, clock, is_fullscreen, sound_manager, highscore_manager, 1)
        
        # If we get here, return to welcome screen

if __name__ == "__main__":
    main()
