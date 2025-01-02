import cv2
import os

def get_next_video_filename(video_folder):
    """
    Determine the next video filename based on the highest existing index in the folder.
    """
    os.makedirs(video_folder, exist_ok=True)
    existing_files = [f for f in os.listdir(video_folder) if f.endswith('.avi')]

    # Extract numeric indices from filenames
    indices = [int(f.split('.')[0]) for f in existing_files if f.split('.')[0].isdigit()]
    next_index = max(indices, default=-1) + 1  # Get the next index (start from 0 if folder is empty)

    return f"{next_index}.avi"

def record_video(video_folder):
    """
    Display webcam feed and start recording video only after pressing the 'r' key.
    If 'd' is pressed, discard the video and stop the program.
    Press 'q' to stop recording and allow new recordings without terminating.
    """
    # Set up video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return None

    # Set a higher resolution explicitly
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1500)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    print(f"Resolution set to: {frame_width}x{frame_height}")
    print("Press 'r' to start recording. Press 'd' to discard the video and stop. Press 'q' to stop recording and reset.")

    while True:
        video_filename = get_next_video_filename(video_folder)
        video_path = os.path.join(video_folder, video_filename)
        
        out = None
        recording = False

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture video frame.")
                break

            # Display the webcam feed
            cv2.imshow("Webcam Feed", frame)

            # If recording has started, write the frame to the video file
            if recording:
                out.write(frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('r') and not recording:
                # Start recording
                out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))
                recording = True
                print(f"Recording started: {video_filename}")

            elif key == ord('d'):
                # Discard the current video and stop the program
                if recording:
                    print(f"Recording discarded. Video file {video_filename} will be deleted.")
                    out.release()  # Release the current video file
                    os.remove(video_path)  # Delete the video file
                cap.release()
                cv2.destroyAllWindows()
                print("Program stopped.")
                return None

            elif key == ord('q'):
                # Stop recording and allow new recordings
                if recording:
                    print("Recording stopped by user.")
                break

        if recording:
            out.release()
            print(f"Video saved to {video_path}")
        else:
            print("No video was recorded.")

        # Check if the user wants to exit the entire program
        print("Press 'ESC' to exit, or any other key to continue.")
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_name = "mopping"  # Change as needed
    video_folder = f"videos/{test_name}"  # Destination folder for videos

    record_video(video_folder)
