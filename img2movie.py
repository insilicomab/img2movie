import glob
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


def create_mp4(select_folder_path, save_file_path):
    filename_list = sorted(glob.glob(f"{select_folder_path}/*.png"))

    img_array = []
    for filename in filename_list:
        """
        日本語の画像ファイルを開くためには、PillowもしくはNumPyで画像ファイルを開いて
        OpenCVの画像データであるNumPyのndarray形式に変換すれば、OpenCVで日本語の画像ファイルを扱える
        """
        pil_img = Image.open(filename)
        img = np.array(pil_img)
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        height, width, _ = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(
        f"{save_file_path}", cv2.VideoWriter_fourcc(*"MP4V"), 10, size
    )

    for i in tqdm(range(len(img_array))):
        out.write(img_array[i])

    out.release()


class Application(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        # ウィンドウの作成
        self.pack()
        self.master.title("動画生成アプリ")
        self.master.iconbitmap("movie.ico")
        self.master.geometry("800x120")
        self.master.resizable(False, False)

        # フレームの作成
        self.input_frame = tk.Frame(self.master)
        self.folder_frame = tk.Frame(self.master)
        self.generate_frame = tk.Frame(self.master)
        self.input_frame.pack()
        self.folder_frame.pack()
        self.generate_frame.pack()

        # フォルダ選択ボタン
        self.select_button = tk.Button(
            self.input_frame, text="フォルダを選択", command=self.select_folder
        )
        self.select_button.pack(pady=10)

        # フォルダ名ラベル
        self.folder_label = tk.Label(self.folder_frame, text="ファイルが選択されていません")
        self.folder_label.pack()

        # 生成ボタン
        self.generate_button = tk.Button(
            self.generate_frame, text="動画生成", command=self.generate_movie
        )
        self.generate_button.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_label.config(text=f"{folder_path}")

    def generate_movie(self):
        # 動画生成ボタンを無効化
        self.generate_button.config(state="disabled")

        # 保存先のファイルパスを取得する
        save_file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")]
        )
        select_folder_path = self.folder_label.cget("text")

        create_mp4(select_folder_path, save_file_path)

        # サブウィンドウ
        subwindow = tk.Toplevel(self.master)
        subwindow.title("サブウィンドウ")
        subwindow.geometry("150x80")
        label = tk.Label(subwindow, text="動画生成が完了しました")
        label.pack(pady=20)

        # 動画生成ボタンを有効化
        self.generate_button.config(state="normal")

        self.folder_label.config(text="ファイルが選択されていません")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    # ループ処理の実行
    root.mainloop()
