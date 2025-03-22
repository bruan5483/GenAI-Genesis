import time
import cv2
import objectDetection
import textToSpeech

def main():
    # Start the object detection and TTS loops
    detection_thread = objectDetection.start_detection()
    tts_thread = textToSpeech.start_tts_loop()
    
    # Create a window in the main thread for display
    cv2.namedWindow("Focused Object Detection", cv2.WINDOW_NORMAL)
    
    while True:
        frame = objectDetection.get_latest_frame()
        if frame is not None:
            focused_object = objectDetection.get_focused_object()
            if focused_object:
                name = focused_object.name
                vertices = [(int(v.x * frame.shape[1]), int(v.y * frame.shape[0]))
                            for v in focused_object.bounding_poly.normalized_vertices]
                if len(vertices) == 4:
                    cv2.rectangle(frame, vertices[0], vertices[2], (0, 255, 0), 2)
                    cv2.putText(frame, name, (vertices[0][0], vertices[0][1]-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Focused Object Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(0.03)  # Small delay for stability
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
