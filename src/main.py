import time
import cv2
import objectDetection
import textToSpeech
import gemini
import threading

def main():
    #print("Starting system...")

    detection_thread = objectDetection.start_detection()
    #print("Object detection started.")

    tts_thread = textToSpeech.start_tts_loop()
    #print("Text-to-speech started.")

    gemini_thread = gemini.start_gemini_loop()
    #print("Gemini processing started.")

    #print("System initialized. Processing video feed...")
    
    while True:
        frame = objectDetection.get_latest_frame()
        if frame is not None:
            focused_object = objectDetection.get_focused_object()
            if focused_object:
                name = focused_object.name
                #print(f"[Main] Detected: {name}")
            
            cv2.imshow("Focused Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting system...")
            break

        time.sleep(0.03)

    cv2.destroyAllWindows()
    print("Windows destroyed. Exiting.")

if __name__ == "__main__":
    main()
