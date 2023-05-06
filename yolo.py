import super_gradients

yolo_nas = super_gradients.training.models.get("yolo_nas_l", pretrained_weights="coco")
prediction = yolo_nas.predict("https://deci-pretrained-models.s3.amazonaws.com/sample_images/beatles-abbeyroad.jpg")

print(prediction.__dir__())
for i in prediction._images_prediction_lst:
    print(i)
    print("\n\n")
