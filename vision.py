import os
# 在导入paddle之前设置环境变量
os.environ["PADDLE_USE_ONEDNN"] = "0" 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import paddlehub as hub


# 加载移动端预训练模型
ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
import cv2
test_img_path = ['tree.png','gold.png']
# 读取测试文件夹test.txt中的照片路径
np_images =[cv2.imread(image_path) for image_path in test_img_path] 

results = ocr.recognize_text(
                    images=np_images,         # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                    use_gpu=True,            # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                    output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                    visualization=True,       # 是否将识别结果保存为图片文件；
                    box_thresh=0.5,           # 检测文本框置信度的阈值；
                    text_thresh=0.5)          # 识别中文文本置信度的阈值；

for result in results:
    data = result['data']
    save_path = result['save_path']
    for infomation in data:
        print('text: ', infomation['text'], '\nconfidence: ', infomation['confidence'], '\ntext_box_position: ', infomation['text_box_position'])
