import cv2
import numpy as np
import os, errno

class ImageEditor:
    def __init__(self, INPUT_FOLDER_PATH, INPUT_FILE_NAME, OUTPUT_FILE_NAME, PADDING_PERCENTANGE, BORDER_PERCENTAGE):
        self.source_file_name = INPUT_FILE_NAME
        self.source_file_path = INPUT_FOLDER_PATH + '/' + self.source_file_name
        self.output_file_path = INPUT_FOLDER_PATH + '/' + OUTPUT_FILE_NAME

        self.PADDING_PERCENTANGE = PADDING_PERCENTANGE
        self.BORDER_PERCENTAGE = BORDER_PERCENTAGE

        self.image = cv2.imread(self.source_file_path)

    def __generate_transparent_background(self, img):
        if img.shape[2] == 4:
            return img

        alpha = np.sum(img, axis=-1) > 0
        alpha = np.uint8(alpha * 255)
        transparent_image = np.dstack((img, alpha))
        return transparent_image

    def __generate_grayscale_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray
    
    def __merge_two_images(self, bg_img, img_to_overlay_t):
        b,g,r,a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b,g,r))
        mask = cv2.medianBlur(a,5)
        img1_bg = cv2.bitwise_and(bg_img.copy(),bg_img.copy(),mask = cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)
        bg_img = cv2.add(img1_bg, img2_fg)

        return bg_img

    def __generate_contour_outline(self, img, border_size):
        gray_image = self.__generate_grayscale_image(self.image)
        _, roi = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        contours = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        output = np.zeros(gray_image.shape, dtype=np.uint8)
        cv2.drawContours(output, contours[0], -1, (255, 255, 255), border_size)

        boundary = 255*np.ones(gray_image.shape, dtype=np.uint8)
        boundary[1:boundary.shape[0]-1, 1:boundary.shape[1]-1] = 0

        toremove = output & boundary
        output = output ^ toremove

        return output

    def __fill_contour_holes(self, gray):
        _, roi = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cv2.drawContours(roi,[cnt],0,255,-1)

        return roi

    def __pixel_distance_furthest_from_center(self, img):
        image_center_coordinates = (img.shape[0] // 2, img.shape[1] // 2)
        height, width = img.shape[:2]

        y, x = np.ogrid[:height, :width]

        distances = np.sqrt(((x - image_center_coordinates[0])**2 + (y - image_center_coordinates[1])**2).astype(np.float32))

        color_mask = img > 0  # Mask for non-zero pixels
        combined = distances * color_mask

        furthest_pixel_idx = np.argmax(combined)
        furthest_pixel_coords = np.unravel_index(furthest_pixel_idx, combined.shape)

        furthest_pixel_distance = distances[furthest_pixel_coords[0], furthest_pixel_coords[1]]

        return furthest_pixel_distance

    def __shrink_canvas_size_by_pixels(self, padding):
        height, width, _ = self.image.shape
        y = 0 + padding
        x = 0 + padding
        padding_height = height  - (padding * 2)
        padding_width = width - (padding * 2)
        cropped_image = self.image[y:y+padding_height, x:x+padding_width]
        cropped_image = self.__generate_transparent_background(cropped_image)
        self.image = cropped_image
      
    def __increase_canvas_size_by_pixels(self, padding):
        image_to_adjust = self.image.copy()
        pad_left, pad_right, pad_top, pad_bot = padding, padding, padding, padding
        larger_image = cv2.copyMakeBorder(image_to_adjust, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=0)
        larger_image = self.__generate_transparent_background(larger_image)
        self.image = larger_image

    def __attempt_file_deletion(self, filename):
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def ensure_square_crop(self):
        height, width, _ = self.image.shape

        if height > width:
            pad_top, pad_bot, pad_left, pad_right=0, 0, int((height - width)/2), int((height - width)/2)
            self.image = cv2.copyMakeBorder(self.image, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=0)
        elif width > height:
            pad_top, pad_bot, pad_left, pad_right=int((width - height)/2), int((width - height)/2), 0, 0
            self.image = cv2.copyMakeBorder(self.image, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=0)

        self.image = self.__generate_transparent_background(self.image)

    def auto_resize_for_padding(self):
        gray_image = self.__generate_grayscale_image(self.image)
        distance = self.__pixel_distance_furthest_from_center(gray_image)

        full_radius = int(self.image.shape[0] / 2)
        actual_padding = int(full_radius - distance)
        target_padding = int(full_radius * self.PADDING_PERCENTANGE)
        padding_adjustment = 0
        if actual_padding < target_padding:
            padding_adjustment = 0 + (target_padding - actual_padding)
        if actual_padding > target_padding:
            padding_adjustment = 0 - (actual_padding - target_padding)

        if padding_adjustment < 0:
            self.__shrink_canvas_size_by_pixels(padding_adjustment * -1)
        else:
            self.__increase_canvas_size_by_pixels(padding_adjustment)

    def add_border_outline(self, should_fill_holes):
        BORDER_SIZE = int(self.image.shape[0] * self.BORDER_PERCENTAGE)
        border_contour_background = self.__generate_contour_outline(self.image, BORDER_SIZE)

        if should_fill_holes:
            border_contour_background = self.__fill_contour_holes(border_contour_background)

        # Convert from grayscale back to color
        cv2.imwrite('gray-temp.png', border_contour_background)
        border_contour_background = cv2.imread('gray-temp.png')
        self.__attempt_file_deletion('gray-temp.png')
    
        logo_foreground = self.image
        merged_image = self.__merge_two_images(border_contour_background, logo_foreground)
        transparent_merged_images = self.__generate_transparent_background(merged_image)

        self.image = transparent_merged_images

    def export_image(self):
        cv2.imwrite(self.output_file_path, self.image)

    # Resizing feature?
    # https://www.youtube.com/watch?v=-LqHr5V67C4
    # https://github.com/aswintechguy/Deep-Learning-Projects/tree/main
    # def enhance_image_resolution(self):
    #     sr = dnn_superres.DnnSuperResImpl_create()
    #     path = 'EDSR_x4.pb'
    #     sr.readModel(path)
    #     # set the model and scale
    #     sr.setModel('edsr', 4)
    #     image = cv2.imread('test.png')
    #     upscaled = sr.upsample(image)
    #     # save the upscaled image
    #     cv2.imwrite('upscaled_test.png', upscaled)