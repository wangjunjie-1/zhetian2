from paddleocr import TextRecognition
model = TextRecognition(model_name=r"PP-OCRv5_server_rec",model_dir=r"./ocr_model/PP-OCRv4_server_rec_doc_infer")
output = model.predict(input="gold.png", batch_size=1)
for res in output:
    res.print()
    res.save_to_img(save_path="./output/")
    res.save_to_json(save_path="./output/res.json")
    
