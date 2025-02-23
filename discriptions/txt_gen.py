import os
image_folder = "/home/kh/AutoChair/chair_image"
if not os.path.exists(image_folder):
    print(f"資料夾 {image_folder} 不存在！")
else:
    for file in os.listdir(image_folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            txt_file = os.path.splitext(file)[0] + ".yaml"
            txt_path = os.path.join("/home/kh/AutoChair/discriptions", txt_file)
            if not os.path.exists(txt_path):
                with open(txt_path, "w", encoding="utf-8") as f:
                    pass
                print(f"success create empty file: {txt_file}")
            else:
                print(f"pass the existed file: {txt_file}")