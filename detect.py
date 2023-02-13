from ultralytics import YOLO
import cv2
import os

SAVE_DIR = 'D:\FaceMaskDetection-Yolov8\Result'

# Load model after training
model = YOLO("D:\\FaceMaskDetection-Yolov8\weights\\best.pt")


def convert_to_list(result):
    # Extract result having tensor.torch form
    tensor = result[0].boxes.boxes

    # Convert tensor.torch to list [x_top_left y_top_left x_bot_right y_bot_right prob labels]
    list_result = tensor.tolist()

    return list_result

def write_result(img_dir):

    img = cv2.imread(img_dir)
    _, width, _ = img.shape
    filename = os.path.basename(img_dir)

    detect = model.predict(source=img_dir) # predict on an image
    list_result = convert_to_list(detect)

    num = 0
    for result in list_result:
        x_top_left, y_top_left, x_bot_right, y_bot_right, prob, label = [result[i] for i in range(len(result))]

        if int(label) == 0:
            text_label = 'NO MASK ' + str(round(prob,2)*100) + '%'
            rgb = (0, 0, 255)
        elif int(label) == 1:
            text_label = 'MASK ' + str(round(prob,2)*100) + '%'
            rgb = (0, 255, 0)
        else:
            text_label = 'WEAR MASK INCORECTLY' + str(round(prob,2)*100) + '%'
            rgb = (0, 69, 255)

        cv2.rectangle(img, (int(x_top_left), int(y_top_left)), (int(x_bot_right), int(y_bot_right)), rgb, 2)

        text_org = (int(x_top_left), int(y_top_left) - 10)
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5 * width / 320
        fontThickness = int(1 * width / 320)

        background_color = rgb
        text_size, _ = cv2.getTextSize(text_label, fontFace, fontScale, fontThickness)

        # Color background
        cv2.rectangle(img, (text_org[0] - 5, text_org[1] - text_size[1] - 5),(text_org[0] + text_size[0] + 5, text_org[1] + 5), background_color, -1)
        cv2.putText(img, text_label, text_org, fontFace, fontScale, (255, 255, 255), fontThickness, cv2.LINE_AA)
        num += 1

    return num, img
    # file_predict = filename + "_predict.png"
    # cv2.imwrite(os.path.join(SAVE_DIR, file_predict), img)

if __name__ == "__main__":

    img_dir = "D:\\ngocson1042002.github.io\\img\\6.jpg"
    # img_dir = "C:\\Users\\ngocs\\Downloads\\1.png"
    # img_dir = "D:\\FaceMaskDetection_Yolov8\\Dataset\\images\\Test\\4_test.png"
    write_result(img_dir)

