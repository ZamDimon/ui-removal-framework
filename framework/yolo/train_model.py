from ultralytics import YOLO

model = YOLO()
model.train(epochs=100, data="config.yaml", name="uis6", pretrained=False)
model.val()
