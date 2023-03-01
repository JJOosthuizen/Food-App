from tkinter import *

import json
import urllib.request
import requests
import components.connect as connect
import io
from PIL import Image, ImageTk


class AppScreen(Tk):
    def __init__(self):
        super().__init__()
        self.title("J-Cuisine!")
        self.geometry("1024x700")
        self.home_screen()

    def home_screen(self):
        """Function that adds all the GUI elements to the homescreen"""
        self.label = Label(self, text="Welcome to J-Cuisine!")
        self.label_search = Label(self, text="Lookup a recipe for...")
        self.label.pack()
        self.label_search.pack()

        self.search_box = Entry(self, width=50)
        self.search_box.pack()

        self.btn_lookup = Button(self, text="Lookup!", command=self.lookup_recipe)
        self.btn_lookup.pack()

    def lookup_recipe(self):
        """Function that looksup 6 results based on user input"""
        connect.fetch_data(self.search_box.get())
        # updating text
        self.label.config(text="Here are 6 result from the search you provided!")
        # removing
        self.label.destroy()
        self.search_box.destroy()
        self.label_search.destroy()
        self.btn_lookup.destroy()
        self.show_result()

    def show_result(self):
        """Function that displays the 6 results to the user"""

        # self.lbl_item1.grid(row=1, column=1, columnspan=4)

        screen_width = 1024
        screen_height = 700
        titles, images = self.read_recipes()

        self.button_list = []
        self.title_list = []
        self.frame_list = []

        for i in range(6):
            # 3 x 3 grid per frame
            self.frame = Frame(
                self,
                width=screen_width / 3,
                height=screen_height / 3,
                bd=1,
                relief="solid",
            )
            self.frame.grid(row=i // 3, column=i % 3, padx=10, pady=5)

            self.frame_label = Label(self.frame, text=titles[i])
            self.frame_label.pack(padx=5, pady=10)
            self.frame_list.append(self.frame)
            self.title_list.append(self.frame_label)
            # image_data = urllib.request.urlopen(images[i]).read()
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(images[i], headers=headers)

            # Open the image using PIL
            recipe_image = Image.open(io.BytesIO(response.content))

            # Convert the PIL image to a Tkinter-compatible format
            tk_image = ImageTk.PhotoImage(recipe_image)

            self.frame_img = Label(self.frame, image=tk_image)
            self.frame_img.image = tk_image  # <== anchor to display image, idk why KEKW
            self.frame_img.pack()

            self.button = Button(
                self.frame,
                text="View Recipe!",
                command=lambda num=i: self.view_recipe(num),
            )
            self.button_list.append(self.button)
            self.button.pack(pady=5)

    def view_recipe(self, button_id):
        """Function that displays the recipe of the dish"""
        # remove old GUI components
        for i in range(len(self.button_list)):
            self.button_list[i].destroy()
            self.title_list[i].destroy()
            self.frame_list[i].destroy()

        try:
            with open("recipes.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            print(e)
        print(button_id)

    def read_recipes(self):
        try:
            titles = []
            images = []
            with open("recipes.json", "r") as f:
                data = json.load(f)
                for recipe in data:
                    titles.append(recipe["title"])
                    images.append(recipe["image"])
            return titles, images
        except FileNotFoundError:
            print("error")


if __name__ == "__main__":
    app = AppScreen()
    app.mainloop()
