import os
import cv2

ROOT_DIR = 'Dataset'
TEST_DIR = os.path.join(ROOT_DIR, 'Test')
TRAIN_DIR = os.path.join(ROOT_DIR, 'Train')
VAL_DIR = os.path.join(ROOT_DIR, 'Validation')


# def rename_file(typeData, dir):

#     dir_with_mask = os.path.join(dir, 'WithMask')
#     list_name_img = os.listdir(dir_with_mask)
#     n = len(list_name_img)

#     for i, img in enumerate(list_name_img):
#         old_file_name = dir_with_mask + '\\' + img
#         new_file_name = dir_with_mask + '\\' + str(i) + '_' + str(typeData) + '.png'
#         os.rename(old_file_name, new_file_name)

#     dir_without_mask = os.path.join(dir, 'WithoutMask')
#     list_name_img = os.listdir(dir_without_mask)
#     for i, img in enumerate(list_name_img):
#         old_file_name = dir_without_mask + '\\' + img
#         new_file_name = dir_without_mask + '\\' + str(i+n) + '_' + str(typeData) + '.png'
#         os.rename(old_file_name, new_file_name)

# rename_file(typeData='test', dir=TEST_DIR)
# rename_file(typeData='train', dir=TRAIN_DIR)
# rename_file(typeData='val', dir=VAL_DIR)

dir_label = os.path.join(ROOT_DIR, 'labels')
if not os.path.exists(dir_label):
    os.makedirs(dir_label)

dir_images = os.path.join(ROOT_DIR, 'images')
if not os.path.exists(dir_images):
    os.makedirs(dir_images)

def create_label(typeData, typeLabel, dir, dir_label, num_with_mask):
    list_name_img = os.listdir(dir)
    list_name_img.sort(key=lambda x: int(x.split('_')[0]))

    for i, img in enumerate(list_name_img):

        if typeLabel == 'WithMask':
            if i == num_with_mask:
                break
        else:
            if i < num_with_mask:
                continue

        if (img.endswith('.png')):

            filename_txt = img.split('.')[0] + '.txt'

            read_img = cv2.imread(os.path.join(dir, img))
            height, width, _ = read_img.shape

            dir_type_data = os.path.join(dir_label, str(typeData))
            if not os.path.exists(dir_type_data):
                os.makedirs(dir_type_data)
                
            f = open(os.path.join(dir_type_data, filename_txt), 'w')

            xmin, ymin, xmax, ymax = 0, 0, width, height
            center_x = (xmin + xmax) / (2 * width)
            center_y = (ymin + ymax) / (2 * height)
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height
            t = '1' if typeLabel == 'WithMask' else '0'
            data = [t, ' ', str(center_x), ' ', str(center_y), ' ', str(bbox_width), ' ', str(bbox_height)]
            f.writelines(data)
            f.close()


if __name__ == '__main__':
    num_test = 992
    num_test_with_mask = 483

    num_train = 10000
    num_train_with_mask = 5000

    num_val = 800
    num_val_with_mask = 400

    create_label(typeLabel='WithMask', typeData='Test', dir_label=dir_label, dir=os.path.join(ROOT_DIR,'images\\Test'), num_with_mask=num_test_with_mask)
    create_label(typeLabel='WithMask', typeData='Train', dir_label=dir_label, dir=os.path.join(ROOT_DIR,'images\\Train'), num_with_mask=num_train_with_mask)
    create_label(typeLabel='WithMask', typeData='Validation', dir_label=dir_label, dir=os.path.join(ROOT_DIR,'images\\Validation'), num_with_mask=num_val_with_mask)


    create_label(typeLabel='WithoutMask', typeData='Test', dir_label=dir_label, dir=os.path.join(ROOT_DIR,'images\\Test'), num_with_mask=num_test_with_mask)
    create_label(typeLabel='WithoutMask', typeData='Train', dir_label=dir_label, dir=os.path.join(ROOT_DIR,'images\\Train'), num_with_mask=num_train_with_mask)
    create_label(typeLabel='WithoutMask', typeData='Validation', dir_label=dir_label, dir=os.path.join(ROOT_DIR,'images\\Validation'), num_with_mask=num_val_with_mask)