from PIL import Image
import os
import math


# 用户输入
def get_user_input():
    img_folder = input("请输入图片文件夹路径: ")
    horizontal_imgs = int(input("请输入每页横向的图片数量: "))
    vertical_imgs = int(input("请输入每页纵向的图片数量: "))
    return img_folder, horizontal_imgs, vertical_imgs


# 函数：创建空白页面
def create_blank_page(page_width, page_height):
    return Image.new("RGB", (page_width, page_height), "white")


# 函数：计算整体居中的起始位置
def calculate_start_position(page_width, page_height, margin, space_between_imgs, horizontal_imgs, vertical_imgs,
                             scaled_img_width, scaled_img_height):
    total_width = horizontal_imgs * scaled_img_width + (horizontal_imgs - 1) * space_between_imgs
    total_height = vertical_imgs * scaled_img_height + (vertical_imgs - 1) * space_between_imgs
    start_x = (page_width - total_width) // 2
    start_y = (page_height - total_height) // 2
    return start_x, start_y


# 函数：计算调整后的图片尺寸
def calculate_scaled_size(img_path, page_width, page_height, margin, space_between_imgs, horizontal_imgs,
                          vertical_imgs):
    with Image.open(img_path) as img:
        img_width, img_height = img.size
    usable_width = page_width - 2 * margin
    usable_height = page_height - 2 * margin
    target_img_width = (usable_width - (horizontal_imgs - 1) * space_between_imgs) / horizontal_imgs
    target_img_height = (usable_height - (vertical_imgs - 1) * space_between_imgs) / vertical_imgs
    scale = min(target_img_width / img_width, target_img_height / img_height)
    return int(img_width * scale), int(img_height * scale)


# 函数：计算图片在页面上的位置，整体居中
def calculate_position_centered(horizontal_imgs, space_between_imgs, scaled_img_width, scaled_img_height, start_x,
                                start_y, img_index):
    row = img_index // horizontal_imgs
    col = img_index % horizontal_imgs
    x = start_x + col * (scaled_img_width + space_between_imgs)
    y = start_y + row * (scaled_img_height + space_between_imgs)
    return x, y


# 函数：生成页面并绘制图片
def generate_pages(img_files, img_folder, page_width, page_height, margin, space_between_imgs, horizontal_imgs,
                   vertical_imgs, scaled_img_width, scaled_img_height, start_x, start_y):
    images_per_page = horizontal_imgs * vertical_imgs
    num_pages = math.ceil(len(img_files) / images_per_page)
    pages = [create_blank_page(page_width, page_height) for _ in range(num_pages)]
    for i, img_file in enumerate(img_files):
        page_index = i // images_per_page
        img_index = i % images_per_page
        x, y = calculate_position_centered(horizontal_imgs, space_between_imgs, scaled_img_width, scaled_img_height,
                                           start_x, start_y, img_index)
        with Image.open(os.path.join(img_folder, img_file)) as img:
            img = img.resize((scaled_img_width, scaled_img_height))
            pages[page_index].paste(img, (x, y))
    return pages


def main():
    img_folder, horizontal_imgs, vertical_imgs = get_user_input()

    # 页面尺寸和边距定义
    page_width, page_height = 2480, 3508  # A4尺寸，像素单位
    margin = 100  # 页边距
    space_between_imgs = 10  # 图片间距

    # 读取文件夹中的所有JPG图片
    img_files = [f for f in os.listdir(img_folder) if f.endswith('.jpg')]
    img_files.sort()  # 按文件名排序

    if img_files:
        # 预先计算调整后的图片尺寸（假设所有图片尺寸相同）
        scaled_img_width, scaled_img_height = calculate_scaled_size(os.path.join(img_folder, img_files[0]), page_width,
                                                                    page_height, margin, space_between_imgs,
                                                                    horizontal_imgs, vertical_imgs)
        start_x, start_y = calculate_start_position(page_width, page_height, margin, space_between_imgs,
                                                    horizontal_imgs, vertical_imgs, scaled_img_width, scaled_img_height)

        # 生成页面
        pages = generate_pages(img_files, img_folder, page_width, page_height, margin, space_between_imgs,
                               horizontal_imgs, vertical_imgs, scaled_img_width, scaled_img_height, start_x, start_y)

        # 保存所有页面
        output_folder = "output_pages"  # 输出文件夹
        os.makedirs(output_folder, exist_ok=True)  # 如果不存在，则创建输出文件夹

        for i, page in enumerate(pages):
            output_path = os.path.join(output_folder, f"page_{i + 1}.png")
            page.save(output_path)
            print(f"页面 {i + 1} 已保存到 {output_path}")

        print("所有页面已成功保存。")
    else:
        print("指定的文件夹没有找到JPG图片，请检查路径或图片格式。")


if __name__ == "__main__":
    main()
