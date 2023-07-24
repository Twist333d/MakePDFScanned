import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import img2pdf
import io
from PIL import ImageEnhance
import random
from PIL import ImageOps

def add_shadow(image):
    # Convert the image to float64
    image = image.astype(np.float64)

    # Create a linear gradient
    gradient = np.linspace(0.5, 1.0, image.shape[1])

    # Apply the gradient to every row of the image
    for i in range(image.shape[0]):
        image[i, :] *= gradient

    # Convert the image back to uint8
    image = image.astype(np.uint8)

    return image

def add_texture(image):
    # Generate random noise as our texture
    texture = np.random.normal(loc=0.5, scale=0.1, size=image.shape) * 255

    # Blend the image and the texture
    image = cv2.addWeighted(image.astype(np.float32), 0.8, texture.astype(np.float32), 0.1, 0.0)

    # Convert the image back to uint8
    image = image.astype(np.uint8)

    return image

def process_pdf(filepath):
    try:
        images = convert_from_path(filepath)
        processed_images = []
        for i, image in enumerate(images):
            # Convert the image to grayscale
            image = image.convert('L')

            # Shrink the image slightly
            width, height = image.size
            image = image.resize((int(width * 0.95), int(height * 0.95)), Image.LANCZOS)

            # Create a new image for border with gradient
            border_image = Image.new('L', (width, height), 255)
            border_data = np.array(border_image)
            gradient = np.linspace(0.7, 1.0, border_data.shape[1])
            for i in range(border_data.shape[0]):
                border_data[i, :] = border_data[i, :] * gradient
            border_image = Image.fromarray(border_data.astype(np.uint8))

            # Paste the original image onto the border image
            border_image.paste(image, (int(width * 0.025), int(height * 0.025)))

            image = border_image

            # Add shadow
            image = add_shadow(np.array(image))

            # Add texture
            image = add_texture(np.array(image))

            # Convert the numpy array back to a PIL Image
            image = Image.fromarray(image)

            # Apply a slight random rotation
            rotation_angle = random.uniform(-5, 5)
            image = image.rotate(rotation_angle, resample=Image.BICUBIC, fillcolor='white')

            # Apply a slight random change in brightness
            brightness_factor = random.uniform(0.85, 1.15)
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)

            # Apply a slight random change in contrast
            contrast_factor = random.uniform(0.85, 1.15)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_factor)

            processed_images.append(image)

        output_filepath = filepath.rsplit('.', 1)[0] + '_scanned.pdf'
        with open(output_filepath, 'wb') as f:
            image_bytes = [io.BytesIO() for _ in processed_images]
            for img, img_byte in zip(processed_images, image_bytes):
                img.save(img_byte, format='JPEG')
                img_byte.seek(0)
            f.write(img2pdf.convert([img_byte.read() for img_byte in image_bytes]))

        return True, 'PDF processed successfully.'

    except Exception as e:
        return False, str(e)