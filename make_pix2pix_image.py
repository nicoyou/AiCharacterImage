import glob
import os
from pathlib import Path

from PIL import Image

# 画像を横に結合する
def hconcat(im1, im2):
	dst = Image.new("RGB", (im1.width + im2.width, im1.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (im1.width, 0))
	return dst

# 画像を縦に結合する
def vconcat(im1, im2):
	dst = Image.new("RGB", (im1.width, im1.height + im2.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (0, im1.height))
	return dst

# 余白を追加してアスペクト比を維持しながら特定のサイズに変換する
def expand2square(pil_img, background_color):
	width, height = pil_img.size
	if width == height:
		return pil_img
	elif width > height:
		result = Image.new(pil_img.mode, (width, width), background_color)
		result.paste(pil_img, (0, (width - height) // 2))
		return result
	else:
		result = Image.new(pil_img.mode, (height, height), background_color)
		result.paste(pil_img, ((height - width) // 2, 0))
		return result

# ファイル名が同じ２枚の画像ペアを結合して教師データを作成する
def make_pix2pix_dataset(input_image_dir, output_image_dir, out_dir = "./"):
	i_images = glob.glob(str(Path(input_image_dir) / "*.*"))
	o_images = glob.glob(str(Path(output_image_dir) / "*.*"))

	os.makedirs(out_dir, exist_ok=True)

	for file_path in i_images:
		file_name = Path(file_path).stem
		img = Image.open(file_path)
		img_resized = expand2square(img, (0, 0, 0)).resize((256, 256))
		try:
			o_img = Image.open([row for row in o_images if Path(row).stem == file_name][0])
		except Exception as e:
			print(e)
			print(file_path)
		o_img_resized = expand2square(o_img, (0, 0, 0)).resize((256, 256))
		result_img = hconcat(o_img_resized, img_resized)
		result_img.save(Path(out_dir) / f"{file_name}.png")

if __name__ == "__main__":
	make_pix2pix_dataset("dataset/original/naked_girl/input", "dataset/original/naked_girl/real", "dataset/out_p2p")
