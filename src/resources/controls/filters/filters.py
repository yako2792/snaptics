import cv2
import numpy as np
from rembg import new_session, remove
from PIL import Image
from src.resources.properties import Properties as Props


session = new_session("isnet-general-use")

class Filter:

    @staticmethod
    def remove_background(image_path, output_path='image_no_background.png'):
        try:
            input = Image.open(image_path)
        except:
            print(f"Image could not be loaded: {image_path}")
            return
        
        output = remove(input, session=session)
        output.save(output_path)

    @staticmethod
    def resize_image(image_path, output_path='resized_image.png'):
        target_resolution = Props.FILTER_RESOLUTION_OUTPUT

        try:
            # Cargar la imagen con PIL y convertirla a RGB
            img = Image.open(image_path).convert("RGB")
        except Exception as e:
            raise ValueError(f"Error al cargar la imagen: {e}")

        # Obtener dimensiones originales
        width, height = img.size

        try:
            target_height = int(target_resolution.lower().replace('p', ''))
        except ValueError:
            raise ValueError("target_resolution debe ser un string como '720p', '480p', etc.")

        # Calcular nueva escala manteniendo el aspecto
        scale = target_height / height
        new_width = int(width * scale)

        # Redimensionar con alta calidad
        resized_img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)

        # Asegurar que la imagen se guarda en PNG
        output_path = output_path if output_path.lower().endswith('.png') else output_path + '.png'
        resized_img.save(output_path, "PNG")

        print(f"Image resized to {new_width}x{target_height} ({target_resolution}, aspect ratio preserved) and saved at: {output_path}")

    @staticmethod
    def fisheye_correction(image_path, output_path='fisheye_corrected.png', k=None, d=None):
        """
        Correct fisheye distortion using camera matrix k and distortion coefficients d.
        If k and d are None, applies a default approximate correction.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")

        h, w = img.shape[:2]

        # Default camera matrix and distortion coefficients for rough correction if none provided
        if k is None or d is None:
            K = np.array([[w, 0, w/2],
                          [0, w, h/2],
                          [0, 0, 1]])
            D = np.array([-0.3, 0.1, 0, 0])
        else:
            K = k
            D = d

        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w, h), np.eye(3), balance=1)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        cv2.imwrite(output_path, undistorted_img)
        print(f"Fisheye distortion corrected and saved at: {output_path}")

    @staticmethod
    def ca_correction(image_path, output_path='ca_corrected.png'):
        """
        Correct chromatic aberration by shifting color channels.
        Simple approximate correction by aligning channels.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")

        b, g, r = cv2.split(img)

        # Shift red and blue channels slightly to correct typical chromatic aberration
        def shift_channel(channel, dx, dy):
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            shifted = cv2.warpAffine(channel, M, (channel.shape[1], channel.shape[0]))
            return shifted

        r_shifted = shift_channel(r, -1, 0)
        b_shifted = shift_channel(b, 1, 0)

        corrected_img = cv2.merge((b_shifted, g, r_shifted))
        cv2.imwrite(output_path, corrected_img)
        print(f"Chromatic aberration corrected and saved at: {output_path}")

    @staticmethod
    def crop_center_object(image_path, width, height, output_path='cropped_image.png', margin=10):
        """
        Crops and centers the main object in an image to a fixed size (width x height) with a white background.
        Ensures at least 'margin' pixels between the object and image borders.
        """
        try:
            input_img = Image.open(image_path).convert("RGBA")
        except Exception as e:
            raise ValueError(f"Could not open image: {e}")

        # Remove background using rembg
        img_no_bg = remove(input_img, session=session)
        img_np = np.array(img_no_bg)

        # Find non-transparent area (bounding box of the object)
        alpha = img_np[:, :, 3]
        non_empty_columns = np.where(alpha.max(axis=0) > 0)[0]
        non_empty_rows = np.where(alpha.max(axis=1) > 0)[0]

        if len(non_empty_columns) == 0 or len(non_empty_rows) == 0:
            raise ValueError("No object detected in the image (fully transparent).")

        left, right = non_empty_columns[0], non_empty_columns[-1]
        top, bottom = non_empty_rows[0], non_empty_rows[-1]

        object_box = img_np[top:bottom+1, left:right+1]
        object_img = Image.fromarray(object_box)

        # Original object size
        obj_width, obj_height = object_img.size

        # Calculate available area (excluding margins)
        target_width = width - 2 * margin
        target_height = height - 2 * margin

        # Compute scaling factor while preserving aspect ratio
        scale = min(target_width / obj_width, target_height / obj_height)
        new_width = int(obj_width * scale)
        new_height = int(obj_height * scale)

        # Resize the object
        resized_object = object_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create white background (RGB)
        background = Image.new("RGB", (width, height), (255, 255, 255))

        # Prepare RGB version of the object (composited onto white)
        object_rgb = Image.new("RGB", resized_object.size, (255, 255, 255))
        object_rgb.paste(resized_object, mask=resized_object.split()[3])  # Use alpha channel as mask

        # Center the object on the canvas
        paste_x = (width - new_width) // 2
        paste_y = (height - new_height) // 2
        background.paste(object_rgb, (paste_x, paste_y))

        # Save final image
        background.save(output_path)
        print(f"Centered and cropped product image saved to: {output_path}")
