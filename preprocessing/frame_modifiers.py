"""Aggregate all simple manipulations on frames."""
import os
import cv2


class FrameModifier:
    @staticmethod
    def crop(image, cols_start_percentage, cols_end_percentage, rows_start_percentage, rows_end_percentage):
        cols_start_index = int(image.shape[1] * cols_start_percentage)
        cols_end_index = int(image.shape[1] * cols_end_percentage)
        rows_start_index = int(image.shape[0] * rows_start_percentage)
        rows_end_index = int(image.shape[0] * rows_end_percentage)
        return image[rows_start_index:rows_end_index, cols_start_index:cols_end_index]

    @staticmethod
    def resize(image, target_size_rows, target_size_cols):
        return cv2.resize(image, (target_size_cols, target_size_rows))


def crop_all_images_for_police():
    all_frames = [x for x in os.listdir("../police_video_frames/") if x.endswith(".png")]
    all_frames.sort(key=lambda x: int(x.split("frame")[-1].split(".png")[0]))

    for frame in all_frames:
        old_image = cv2.imread(f"police_video_frames/{frame}")
        cropped_image = FrameModifier.crop(old_image, 0.3, 0.9, 0.05, 0.55)
        cv2.imwrite(f"police_video_frames/cropped/{frame}", cropped_image)


def generate_resized_image1000():
    original_frame = cv2.imread(f"police_video_frames/frame1000.png")
    cropped_frame = FrameModifier.crop(original_frame, 0.3, 0.9, 0.05, 0.55)
    resized = FrameModifier.resize(cropped_frame, cropped_frame.shape[0] * 2, cropped_frame.shape[1] * 2)
    cv2.imwrite(f"simple_resized_frame1000.png", resized)

def generate_resized_image(image_id):
    original_frame = cv2.imread(f"police_video_frames/frame{image_id}.png")
    cropped_frame = FrameModifier.crop(original_frame, 0.3, 0.9, 0.05, 0.55)
    resized = FrameModifier.resize(cropped_frame, cropped_frame.shape[0] * 2, cropped_frame.shape[1] * 2)
    cv2.imwrite(f"simple_resized_frame{image_id}.png", resized)
