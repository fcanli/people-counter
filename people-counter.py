import cv2
import numpy as np

# YOLO modelini yükle
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

cap = cv2.VideoCapture("IMG_0093-720p.mp4")
line_x = 600  # Dikey çizgi x koordinatı (kamera çözünürlüğüne göre ayarlayın)
girenler = 0
cikanlar = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # YOLO ile nesne tespiti
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    insanlar = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id == 0 and confidence > 0.5:  # 0: 'person' sınıfı
                merkez_x = int(detection[0] * width)  # X koordinatı önemli
                merkez_y = int(detection[1] * height)
                insanlar.append((merkez_x, merkez_y))

    # Yön tespiti (DİKEY ÇİZGİ)
    girenler = 0
    cikanlar = 0
    for (x, y) in insanlar:
        if x < line_x:  # Çizginin solundan sağına geçerse "GİREN"
            girenler += 1
        else:           # Çizginin sağından soluna geçerse "ÇIKAN"
            cikanlar += 1

    # Görselleştirme (Dikey çizgi)
    cv2.line(frame, (line_x, 0), (line_x, height), (0, 255, 0), 2)  # Dikey çizgi
    cv2.putText(frame, f"Soldakiler: {girenler}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Sagdakiler: {cikanlar}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("AI Sayim", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()