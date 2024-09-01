import os
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap

def random_image_from_folder(folder_path="/Users/yulingx/Downloads/anime"):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Filter for image files (you can add more extensions if needed)
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    image_files = [f for f in files if f.lower().endswith(image_extensions)]
    
    # Check if there are any image files in the folder
    if not image_files:
        return None
    
    # Randomly select an image file
    random_image = random.choice(image_files)
    
    # Return the full path of the selected image
    return os.path.join(folder_path, random_image)

def add_text_to_image(image_path, text, font_size=36):
    # Open the image
    img = Image.open(image_path)
    
    # Create a drawing object
    draw = ImageDraw.Draw(img)
    
    # Choose Disney-style font
    font_path = "/Users/yulingx/Downloads/cursor_example/waltograph/waltographUI.ttf"  # Make sure this file is in the same directory as your script
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Disney font not found. Using default font.")
        font = ImageFont.load_default()
    
    # Get image size
    img_w, img_h = img.size
    
    # Calculate maximum width for text (80% of image width)
    max_width = int(img_w * 0.8)
    
    # Function to wrap text and calculate size
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_w, _ = draw.textsize(test_line, font=font)
            if test_w <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return '\n'.join(lines)
    
    # Adjust font size and wrap text
    while font_size > 8:
        font = ImageFont.truetype(font_path, font_size)
        wrapped_text = wrap_text(text, font, max_width)
        text_w, text_h = draw.multiline_textsize(wrapped_text, font=font)
        if text_w <= max_width and text_h <= img_h * 0.9:
            break
        font_size -= 1
    
    # Calculate text position (left-aligned and vertically centered)
    text_position = (int(img_w * 0.1), (img_h - text_h) // 2)
    
    # Add text to the image
    draw.multiline_text(text_position, wrapped_text, font=font, fill=(255, 255, 255), align='left')
    
    # Create 'modified' subfolder if it doesn't exist
    output_folder = os.path.join(os.path.dirname(image_path), "modified")
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the modified image in the 'modified' subfolder
    output_filename = os.path.basename(image_path)
    output_path = os.path.join(output_folder, f"modified_{output_filename}")
    img.save(output_path)
    
    # Preview the image
    img.show()
    
    return output_path

# Example usage
selected_image = random_image_from_folder()
if selected_image:
    user_text = input("Enter the text you want to add to the image: ")
    user_font_size = input("Enter the font size (press Enter for default 36): ")
    
    # Use the default size if the user doesn't input a valid number
    try:
        font_size = int(user_font_size) if user_font_size else 36
    except ValueError:
        font_size = 36
    
    modified_image = add_text_to_image(selected_image, user_text, font_size)
    print(f"Image with added text saved as: {modified_image}")
else:
    print("No image files found in the specified folder.")
