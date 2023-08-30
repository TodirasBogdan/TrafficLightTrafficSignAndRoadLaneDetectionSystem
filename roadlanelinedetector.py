import numpy as np
import cv2


def mask_region_of_interest(image):
    # Define region of interest polygon
    width = image.shape[1]
    height = image.shape[0]
    region_of_interest = np.array([[(width * 0.40, height * 0.70), (width * 0.55, height * 0.70),
                                    (width * 0.75, height * 0.9), (width * 0.20, height * 0.9)]],
                                  dtype=np.int32)
    # Create a black mask
    mask = np.zeros_like(image)
    # Apply white region of interest to black mask
    cv2.fillPoly(mask, region_of_interest, color=255)
    # Apply mask with region of interest to original image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def make_coordinates(image, line_parameters):
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = [0.001, 0]
    y1 = image.shape[0]
    y2 = int(y1 * 0.75)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_lines(image, lines):
    left_fit = []
    right_fit = []
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                parameters = np.polyfit(x=(x1, x2), y=(y1, y2), deg=1)
                slope = parameters[0]
                intercept = parameters[1]
                if slope < 0:
                    left_fit.append((slope, intercept))
                else:
                    right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


def draw_lines(image, lines):
    # Create black image
    black_line_image = np.zeros_like(image)
    lines = np.asarray(lines, dtype=int)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            # Draw lines on black image
            cv2.line(black_line_image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=5)
        # Add lines to original image
        image = cv2.addWeighted(image, 0.8, black_line_image, 1, gamma=0)
    return image


def process_frame(image):
    # Convert image to grayscale
    gray_scale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Apply Gaussian filter to image
    blur_image = cv2.GaussianBlur(src=gray_scale_image, ksize=(5, 5), sigmaX=0)
    # Find edges in image
    canny_image = cv2.Canny(image=blur_image, threshold1=50, threshold2=100)
    # Mask the image with region of interest
    masked_image = mask_region_of_interest(image=canny_image)
    # Find best lines in Hough space
    lines = cv2.HoughLinesP(image=masked_image, rho=1, theta=np.pi / 720, threshold=100, lines=np.array([]),
                            minLineLength=50, maxLineGap=50)
    # Average the lines
    averaged_lines = average_lines(image, lines)
    # Draw averaged lines on the image
    lined_image = draw_lines(image, averaged_lines)

    return lined_image
