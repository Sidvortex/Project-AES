
import time
import cv2
import numpy as np
from emotion.camera import CameraCapture    
from emotion.face import FaceEmotionDetector     
from emotion.analyzer import EmotionAnalyzer


SIDE_PANEL_WIDTH = 320
WINDOW_NAME = "JARVIS - Emotion Viewer (press q to quit)"
FRAME_SCALE = 1.0   

def make_side_panel(frame_h, emotions_dict, dominant, confidence):
    """Create a side panel image showing emotion bars and dominant emotion."""
    panel = np.ones((frame_h, SIDE_PANEL_WIDTH, 3), dtype=np.uint8) * 230 

   
    cv2.putText(panel, "Emotion Panel", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (10,10,10), 2)

    
    cv2.putText(panel, f"Dominant: {dominant}", (12, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    cv2.putText(panel, f"Confidence: {confidence:.2f}", (12, 88), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,50,50), 1)

    
    start_y = 120
    bar_h = 26
    padding = 10
    max_bar_w = SIDE_PANEL_WIDTH - 140

   
    items = sorted(emotions_dict.items(), key=lambda x: -x[1])
    for i, (emo, val) in enumerate(items):
        y = start_y + i * (bar_h + padding)
        label = f"{emo}"
        score_text = f"{val:.2f}"
        cv2.putText(panel, label, (12, y + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (10,10,10), 1)
        # bar bg
        cv2.rectangle(panel, (110, y + 6), (110 + max_bar_w, y + 6 + bar_h), (200,200,200), -1)
        # bar fill
        fill_w = int(max_bar_w * float(val))
        cv2.rectangle(panel, (110, y + 6), (110 + fill_w, y + 6 + bar_h), (80,150,255), -1)
        # score
        cv2.putText(panel, score_text, (110 + max_bar_w + 8, y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20,20,20), 1)

    return panel

def main():
    print("Starting JARVIS Emotion Viewer...")
    
    camera = CameraCapture()
    face_detector = FaceEmotionDetector()
    analyzer = EmotionAnalyzer()   

    
    try:
        camera.start()
    except Exception as e:
        print("Camera start failed:", e)
        return

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    try:
        while True:
            frame_data = camera.get_latest_frame()
            if frame_data is None:
               
                time.sleep(0.03)
                continue

            frame, ts = frame_data
            
            if FRAME_SCALE != 1.0:
                frame = cv2.resize(frame, (0,0), fx=FRAME_SCALE, fy=FRAME_SCALE)

            
            try:
                detection = face_detector.detect(frame)
            except Exception as e:
                detection = None
                print("Face detect error:", e)

            
            emotions = { 'neutral': 0.0 }
            dominant = 'N/A'
            conf = 0.0

            if detection:
                if detection.get('face_detected', True) and detection.get('emotions'):
                    emotions = detection.get('emotions', {})
                    emotions = {k: float(v) for k, v in emotions.items()}
                    dominant = detection.get('primary_emotion') or detection.get('dominant_emotion') or dominant
                    conf = float(detection.get('confidence', 0.0))
                    analyzer.add_face_detection({
                        'dominant_emotion': dominant,
                        'emotions': emotions,
                        'confidence': conf,
                        'face_detected': True,
                        'timestamp': time.time()
                    })
                    smoothed = analyzer.get_current_emotion()
                    if smoothed:
                        dominant = smoothed.get('primary_emotion', dominant)
                        conf = smoothed.get('confidence', conf)
                else:
                    dominant = 'No face'
                    emotions = { 'neutral': 1.0 }
                    conf = 0.0

            h, w = frame.shape[:2]
            panel = make_side_panel(h, emotions, dominant, conf)

            try:
                combined = np.hstack((frame, panel))
            except Exception:
                panel = cv2.resize(panel, (SIDE_PANEL_WIDTH, h))
                combined = np.hstack((frame, panel))

            cv2.imshow(WINDOW_NAME, combined)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping...")
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
