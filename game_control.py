import cv2
import mediapipe as mp
import pydirectinput  # DirectInput for handling hardware-level keypresses in 3D games
import time

# --- SAFETY PAUSE ADDITION ---
# Adds a 0.05-second buffer to keystrokes so the game registers them properly
pydirectinput.PAUSE = 0.05  

# Initialize MediaPipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,              # Track only one hand for gameplay
    min_detection_confidence=0.7, # Higher confidence lowers input jitter
    min_tracking_confidence=0.7
)

# Open webcam feed
cap = cv2.VideoCapture(0)

# Landmark IDs for finger tips and their corresponding lower joints (PIP joints)
finger_tip_ids = [8, 12, 16, 20]
finger_pip_ids = [6, 10, 14, 18]

current_key = None

def press_only(key):
    """Helper function to release the old key and hold down the new key smoothly"""
    global current_key
    if current_key != key:
        if current_key:
            pydirectinput.keyUp(current_key)  # Release the previous action
        if key:
            pydirectinput.keyDown(key)        # Hold down the new action
        current_key = key

print("Asphalt 8 Controller Ready! Open your game and show your hand to the webcam.")
print("Press 'q' in the webcam window to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the frame horizontally for a natural mirror-view effect
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # Convert image from BGR to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    action_text = "COASTING (Neutral)"
    detected_action = None

    if results.multi_hand_landmarks:
        # Loop through hand landmarks and their corresponding handedness (Left/Right)
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            
            # Draw the hand skeleton tracking points on the screen
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract landmarks into a list of pixel coordinates (X, Y)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append((int(lm.x * w), int(lm.y * h)))

            # Get Hand Label ('Left' or 'Right')
            hand_label = handedness.classification[0].label

            # Check individual state of the 4 fingers (True if UP)
            index_up = landmarks[8][1] < landmarks[6][1]
            middle_up = landmarks[12][1] < landmarks[10][1]
            ring_up = landmarks[16][1] < landmarks[14][1]
            pinky_up = landmarks[20][1] < landmarks[18][1]
            
            # Check Thumb state dynamically based on which hand is visible
            thumb_up = False
            if hand_label == "Right":
                if landmarks[4][0] < landmarks[3][0]:  
                    thumb_up = True
            else:
                if landmarks[4][0] > landmarks[3][0]:  
                    thumb_up = True

            # Calculate total active fingers up
            total_fingers = sum([index_up, middle_up, ring_up, pinky_up, thumb_up])

            # --- GAME GESTURE CONTROLLER MAPPING ---
            if total_fingers == 0:
                action_text = "ACCELERATE (W)"
                detected_action = 'w'
            elif total_fingers == 5:
                action_text = "BRAKE / REVERSE (S)"
                detected_action = 's'
            elif total_fingers == 1:
                action_text = "STEER LEFT (A)"
                detected_action = 'a'
            elif total_fingers == 2:
                action_text = "STEER RIGHT (D)"
                detected_action = 'd'
            else:
                action_text = "NEUTRAL"
                detected_action = None

    else:
        action_text = "NO HAND DETECTED"
        detected_action = None

    # Apply the simulated hardware input to your active window
    press_only(detected_action)

    # Display visual overlay control dashboard
    cv2.rectangle(frame, (10, 15), (480, 75), (0, 0, 0), -1)
    cv2.putText(frame, action_text, (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    # --- FLOATING ALWAYS-ON-TOP WINDOW FIX ---
    # These lines force the webcam panel to float on top of the Asphalt 8 window
    cv2.namedWindow("Asphalt 8 Controller Window", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("Asphalt 8 Controller Window", cv2.WND_PROP_TOPMOST, 1)
    
    # Show live webcam status window
    cv2.imshow("Asphalt 8 Controller Window", frame)

    # Break loop cleanly by pressing 'q' while focusing the webcam window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Safely release any stuck keys before shutting down
if current_key:
    pydirectinput.keyUp(current_key)

cap.release()
cv2.destroyAllWindows()