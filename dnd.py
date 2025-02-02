import pygame
import random

pygame.init()

# Window dimensions
width, height = 1200, 800  # Adjusted to 1200x800 as requested
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drag and Drop Vocabulary Puzzle")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Font
font_size = 24
font = pygame.font.Font(None, font_size)
message_font = pygame.font.Font(None, 36)

# Vocabulary words and definitions
vocab = {
    "Serendipity": "The occurrence and development of events by chance in a happy or beneficial way.",
    "Ephemeral": "Lasting for a very short time.",
    "Ubiquitous": "Present, appearing, or found everywhere.",
    "Mellifluous": "(of a voice or words) sweet or musical; pleasant to hear.",
    "Obsequious": "Excessively attentive or flattering.",
    "Pernicious": "Having a harmful effect, especially in a gradual or subtle way.",
    "Gregarious": "Fond of company; sociable.",
    "Laconic": "Using very few words.",
}

# Prepare word/definition pairs
pairs = list(vocab.items())
random.shuffle(pairs)

# Lists to store surfaces and rects
word_rects = []
def_rects = []
word_surfaces = []
def_surfaces = []
word_original_positions = []
word_colors = {}
matched_words = {}

x_word = 50
x_def = 400
y_start = 50
y_spacing = 100  # Increased spacing between words to prevent overlap
line_width = (
    width - x_def - 50
)  # Adjusted to use most of the available space minus margins


# Function to render wrapped text
def render_wrapped_text(text, font, color, max_width, start_pos):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_surface = font.render(test_line, True, color)
        if test_surface.get_width() > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    lines.append(current_line)  # Append last line

    surfaces = []
    for i, line in enumerate(lines):
        surfaces.append(
            (
                font.render(line, True, color),
                (start_pos[0], start_pos[1] + i * (font.get_height() + 5)),
            )
        )

    return surfaces


# Initialize word positions and define original colors
for word, definition in pairs:
    word_surface = font.render(word, True, black)
    word_surfaces.append(word_surface)

    word_rect = word_surface.get_rect(topleft=(x_word, y_start))
    word_rects.append(word_rect)

    def_rect = pygame.Rect(x_def, y_start, line_width, font_size)
    def_rects.append(def_rect)

    word_original_positions.append(word_rect.topleft)
    word_colors[word] = black
    matched_words[word] = False

    y_start += y_spacing

# Dragging variables
dragging = False
selected_rect = None
offset = (0, 0)
selected_index = None

# Message variables
message = ""
message_color = black
message_timer = 0  # Frames left to display message

# Button
button_font = pygame.font.Font(None, 32)
button_text = button_font.render("Finish", True, white)
button_width, button_height = button_text.get_size()
button_rect = pygame.Rect(
    width - button_width - 5,
    height - button_height - 5,
    button_width + 20,
    button_height + 20,
)

# Game loop
running = True
while running:
    screen.fill(white)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(word_rects):
                    if rect.collidepoint(event.pos) and not matched_words[pairs[i][0]]:
                        dragging = True
                        selected_rect = rect
                        offset = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                        selected_index = i
                        break

                # Check if the finish button was clicked
                if button_rect.collidepoint(event.pos):
                    running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                dragging = False
                if selected_rect in word_rects:
                    correct_match = False
                    for j, def_rect in enumerate(def_rects):
                        blank_space = pygame.Rect(
                            def_rect.left - line_width - 10,
                            def_rect.top,
                            line_width,
                            def_rect.height,
                        )
                        if blank_space.colliderect(selected_rect):
                            word, definition = pairs[selected_index]
                            correct_word, correct_def = pairs[j]
                            if word == correct_word and not matched_words[word]:
                                print("Correct!")
                                correct_match = True
                                matched_words[word] = True
                                word_colors[word] = (
                                    green  # Mark original location green
                                )

                                # Move word up slightly for proper alignment
                                selected_rect.topleft = (
                                    blank_space.left + 10,
                                    blank_space.bottom - selected_rect.height - 5,
                                )

                                message = "Correct!"
                                message_color = green
                                message_timer = 180  # Display for 3 seconds

                                break

                    if not correct_match:
                        print("Incorrect!")
                        selected_rect.topleft = word_original_positions[selected_index]
                        word_colors[pairs[selected_index][0]] = (
                            red  # Mark original location red
                        )

                        message = "Incorrect!"
                        message_color = red
                        message_timer = 180  # Display for 3 seconds

                selected_rect = None

        if event.type == pygame.MOUSEMOTION:
            if dragging and selected_rect is not None:
                selected_rect.topleft = (
                    event.pos[0] - offset[0],
                    event.pos[1] - offset[1],
                )

    # Draw words and definitions
    for i in range(len(word_rects)):
        # Adjust underline position to be 7 characters long before the definition
        underline_start = (
            def_rects[i].left - 7 * font.size("W")[0]
        )  # Move 7 characters to the left
        underline_end = def_rects[i].left  # Ends at the start of the definition

        pygame.draw.line(
            screen,
            black,
            (underline_start, def_rects[i].centery),
            (underline_end, def_rects[i].centery),
            2,
        )

        screen.blit(word_surfaces[i], word_rects[i])

        # Wrap long definitions
        wrapped_text_surfaces = render_wrapped_text(
            pairs[i][1], font, black, line_width - 20, def_rects[i].topleft
        )
        for surface, pos in wrapped_text_surfaces:
            screen.blit(surface, pos)

    # Display feedback message
    if message_timer > 0:
        message_surface = message_font.render(message, True, message_color)
        screen.blit(
            message_surface,
            (width // 2 - message_surface.get_width() // 2, height - 100),
        )
        message_timer -= 1

    # Draw the finish button
    # Calculate the button's position so it's right-aligned
    button_x = width - button_width - 30 # 5 pixels from the right
    button_y = height - button_height - 30  # 5 pixels from the bottom

    button_rect = pygame.Rect(button_x, button_y, button_width + 20, button_height + 20)

    # Draw the finish button
    pygame.draw.rect(screen, blue, button_rect)
    screen.blit(button_text, (button_x + 10, button_y + 10))
    # Ensure finish button is not overlapping the definitions
    if def_rects and def_rects[-1].bottom + 50 > button_rect.top:
        button_rect.top = def_rects[-1].bottom + 10

    pygame.display.flip()

pygame.quit()
