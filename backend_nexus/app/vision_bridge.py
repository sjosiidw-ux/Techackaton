import logging

# Lazy-import heavy/native libs so the backend can start in minimal environments
try:
    import cv2
except Exception:
    cv2 = None

# Lazy-import YOLO to avoid hard dependency at module-import time
try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

class NexusVision:
    #def __init__(self, model_path="models/yolo11n_idd_finetuned.pt", video_source="traffic_sample.mp4"):
    def __init__(self, model_path="yolo11n.pt", source=0):
        self.active = False
        try:
            # Source 164: Load fine-tuned model (lazy-loaded)
            if YOLO is None:
                raise ImportError("ultralytics not installed")
            self.model = YOLO(model_path)
            self.source = source
            self.active = True
        except Exception as e:
            print(f"⚠️ YOLO Model not found. Running in Logic-Only mode. ({e})")

    def get_real_world_density(self):
        """
        Runs inference on the camera feed to get real vehicle counts.
        (Source 163 in PDF)
        """
        if not self.active:
            return 0
        
        # Grab a single frame from the camera/video
        cap = cv2.VideoCapture(self.source)
        ret, frame = cap.read()
        if ret:
            results = self.model(frame, verbose=False)
            # Count bounding boxes (Source 169)
            density = len(results[0].boxes)
            cap.release()
            return density
        return 0