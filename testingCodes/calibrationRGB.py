import cv2
import numpy as np
import csv
import os

colorArray = ["Blue", "Red", "Green", "Yellow"]
grab_area = [200, 370, 440, 480]

def getframes(cap):
    ret, frame = cap.read()
    if ret:
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        box_size = 70  # Size of the central box
        x_center, y_center = width // 2, height // 2
        x1, y1 = x_center - box_size // 2, y_center - box_size // 2
        x2, y2 = x_center + box_size // 2, y_center + box_size // 2
        
        # Draw the center box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Extract the region of interest (ROI)
        roi = frame[y1:y2, x1:x2]
        
        # Calculate the average RGB value inside the box
        avg_rgb = np.mean(roi, axis=(0, 1))
        
        # Display RGB values on the frame
        text = f"R: {int(avg_rgb[0])}, G: {int(avg_rgb[1])}, B: {int(avg_rgb[2])}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.line(frame, (0, 340), (width, 340), (255, 0, 0), 2)
        cv2.rectangle(frame, (int(grab_area[0]), int(grab_area[1])), (int(grab_area[2]), int(grab_area[3])), (255, 255, 255), 1)
        fframe=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Show the frame
        cv2.imshow("Camera Feed", fframe)
        return avg_rgb
    else:
        return None

def main():
    global colorArray
    cap = cv2.VideoCapture(0)  # Open the default camera
    csv_file = "captured_rgb_data.csv"
    
    # Create CSV file if it doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Color", "R", "G", "B"])

    while True:
        avg_rgb = getframes(cap)
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(10) & 0xFF == ord('p'):
            if len(colorArray) != 0:
                color = colorArray.pop(0)
                for i in range(20):
                    avg_rgb = getframes(cap)
                    # Append data to CSV file
                    with open(csv_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([color, int(avg_rgb[0]), int(avg_rgb[1]), int(avg_rgb[2])])
                        print(f"{color} color Taken")
            else:
                colorArray = ["Blue", "Red", "Green", "Yellow"]

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
