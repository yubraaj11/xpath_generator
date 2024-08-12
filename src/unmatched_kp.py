import cv2
import numpy as np
from matplotlib import pyplot as plt


def draw_keypoints(image, keypoints, color=(0, 255, 0)):
    # Draw keypoints on the image
    img_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=color, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return img_with_keypoints


def find_and_draw_differences(img1_path, img2_path):
    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Detect keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Matched keypoints
    matched_kp1 = [kp1[m.queryIdx] for m in matches]
    matched_kp2 = [kp2[m.trainIdx] for m in matches]

    # Find unmatched keypoints
    unmatched_kp1 = [kp for kp in kp1 if kp not in matched_kp1]
    unmatched_kp2 = [kp for kp in kp2 if kp not in matched_kp2]

    # Matched keypoints
    img1_with_matched = draw_keypoints(img1, matched_kp1, color=(255, 0, 0))
    img2_with_matched = draw_keypoints(img2, matched_kp2, color=(255, 0, 0))

    # Display images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img1_with_matched, cv2.COLOR_BGR2RGB))
    plt.title('matched Keypoints in Image 1')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img2_with_matched, cv2.COLOR_BGR2RGB))
    plt.title('matched Keypoints in Image 2')
    plt.axis('off')
    plt.savefig('../output_image/matched_2.jpg')

    # Unmatched keypoints
    img1_with_unmatched = draw_keypoints(img1, unmatched_kp2, color=(0, 0, 255))
    img2_with_unmatched = draw_keypoints(img2, unmatched_kp2, color=(0, 0, 255))

    # Display images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img1_with_unmatched, cv2.COLOR_BGR2RGB))
    plt.title('Unmatched Keypoints in Image 1')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img2_with_unmatched, cv2.COLOR_BGR2RGB))
    plt.title('Unmatched Keypoints in Image 2')
    plt.axis('off')
    plt.savefig('../output_image/unmatched_2.jpg')

    plt.show()


# Example usage
find_and_draw_differences('/home/yubraj/Documents/vertex-projects/omniglue/res/ss4.png',
                          '/home/yubraj/Documents/vertex-projects/omniglue/res/ss6.png')
