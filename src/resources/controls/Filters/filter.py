import cv2
import numpy as np

class Filter:

    @staticmethod
    def remove_background(image_path, output_path='image_no_background.png'):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Range for all light colors (not just gray)
        lower_bg = np.array([0, 0, 90])
        upper_bg = np.array([180, 60, 255])

        mask_bg = cv2.inRange(hsv, lower_bg, upper_bg)
        mask_obj = cv2.bitwise_not(mask_bg)

        # Refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask_clean = cv2.morphologyEx(mask_obj, cv2.MORPH_OPEN, kernel)
        mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

        # Flood fill holes inside the mask to fill gaps with white
        floodfilled = mask_clean.copy()
        h, w = mask_clean.shape[:2]
        mask_floodfill = np.zeros((h + 2, w + 2), np.uint8)

        cv2.floodFill(floodfilled, mask_floodfill, (0, 0), 255)

        holes = cv2.bitwise_not(floodfilled)
        mask_filled = cv2.bitwise_or(mask_clean, holes)

        mask_blur = cv2.GaussianBlur(mask_filled, (7, 7), 0)
        alpha = cv2.normalize(mask_blur, None, 0, 255, cv2.NORM_MINMAX)

        b, g, r = cv2.split(img)
        img_rgba = cv2.merge((b, g, r, alpha.astype(np.uint8)))

        cv2.imwrite(output_path, img_rgba)
        print(f"Image saved without background and holes filled at: {output_path}")

    @staticmethod
    def resize_image(image_path, output_path='resized_image.png', target_resolution='480p'):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")

        height, width = img.shape[:2]

        try:
            target_height = int(target_resolution.lower().replace('p', ''))
        except ValueError:
            raise ValueError("target_resolution must be a string like '720p', '480p', etc.")

        scale = target_height / height
        new_width = int(width * scale)
        new_height = target_height

        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(output_path, resized_img)
        print(f"Image resized to {new_width}x{new_height} ({target_resolution}, aspect ratio preserved) and saved at: {output_path}")

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
            # Assume some generic fisheye parameters
            K = np.array([[w, 0, w/2],
                          [0, w, h/2],
                          [0, 0, 1]])
            D = np.array([-0.3, 0.1, 0, 0])  # typical fisheye distortion coefficients
        else:
            K = k
            D = d

        # Create new camera matrix
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w,h), np.eye(3), balance=1)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, (w,h), cv2.CV_16SC2)
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

        # Shift red and blue channels slightly to correct typical CA
        # Values can be tuned for better correction
        def shift_channel(channel, dx, dy):
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            shifted = cv2.warpAffine(channel, M, (channel.shape[1], channel.shape[0]))
            return shifted

        r_shifted = shift_channel(r, -1, 0)
        b_shifted = shift_channel(b, 1, 0)

        corrected_img = cv2.merge((b_shifted, g, r_shifted))

        cv2.imwrite(output_path, corrected_img)
        print(f"Chromatic aberration corrected and saved at: {output_path}")
