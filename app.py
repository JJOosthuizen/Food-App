from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
import json
import re
import requests
import components.connect as connect
import io
from PIL import Image, ImageTk


class AppScreen(Tk):
    def __init__(self):
        super().__init__()
        self.title("J-Cuisine!")
        self.screen_width = 1024
        self.screen_height = 700
        self.geometry("1024x700")
        self.home_screen()

    def home_screen(self):
        """Function that adds all the GUI elements to the homescreen"""
        self.label = Label(
            self, text="Welcome to J-Cuisine!", pady=15, font=("Arial", 20, "italic")
        )
        self.label_search = Label(
            self, text="Lookup a recipe for...", font=("Arial", 12, "bold"), pady=5
        )
        self.label.pack()
        self.label_search.pack()

        self.search_box = Entry(self, width=50)
        self.search_box.pack()

        self.btn_lookup = Button(self, text="Lookup!", command=self.lookup_recipe)
        self.btn_lookup.pack()

        self.lbl_note = Label(
            self,
            text="Note that when the field is open that it will give random recipes",
            font=("Arial", 8, "italic bold underline"),
            pady=10,
            underline=0,
        )

        self.lbl_note.pack()

    def lookup_recipe(self):
        """Function that looksup 6 results based on user input"""
        connect.fetch_data(self.search_box.get())
        # updating text
        # self.label.config(text="Here are 6 result from the search you provided!")
        # removing
        self.label.destroy()
        self.search_box.destroy()
        self.label_search.destroy()
        self.btn_lookup.destroy()
        self.lbl_note.destroy()
        self.show_result()

    def show_result(self):
        """Function that displays the 6 results to the user"""
        titles, images = self.read_recipes()

        self.button_list = []
        self.title_list = []
        self.frame_list = []
        self.frame_img_list = []
        for i in range(6):
            # 3 x 3 grid per frame
            self.frame = Frame(
                self,
                width=self.screen_width / 3,
                height=self.screen_height / 3,
                bd=1,
                relief="solid",
            )
            self.frame.grid(row=i // 3, column=i % 3, padx=10, pady=5)

            self.frame_label = Label(
                self.frame, text=titles[i], font=("Arial", 12, "bold"), wraplength=200
            )
            self.frame_label.pack(padx=5, pady=10)
            self.frame_list.append(self.frame)
            self.title_list.append(self.frame_label)

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(images[i], headers=headers)

            # Open the image using PIL
            recipe_image = Image.open(io.BytesIO(response.content))

            # Convert the PIL image to a Tkinter-compatible format
            self.tk_image = ImageTk.PhotoImage(recipe_image)

            self.frame_img = Label(self.frame, image=self.tk_image)
            self.frame_img.image = self.tk_image  # <== anchor to display image
            self.frame_img.pack()
            self.frame_img_list.append(self.tk_image)

            self.button = Button(
                self.frame,
                text="View Recipe!",
                command=lambda btn_id=i: self.view_recipe(btn_id),
            )
            self.button_list.append(self.button)
            self.button.pack(pady=5)

    def view_recipe(self, button_id):
        """Function that displays the recipe of the dish"""
        self.make_view_recipe_GUI(button_id)

    def make_view_recipe_GUI(self, button_id):
        """Function that creates the GUI for viewing a dish"""

        # remove old GUI components
        for i in range(len(self.button_list)):
            self.button_list[i].destroy()
            self.title_list[i].destroy()
            self.frame_list[i].destroy()

        self.load_frame = Frame(width=self.screen_width, height=self.screen_height / 2)
        self.load_frame.grid(row=1, column=1, columnspan=2, pady=10)
        self.progressbar = ttk.Progressbar(
            self.load_frame, orient="horizontal", length=200, mode="indeterminate"
        )
        self.progressbar.pack()
        self.progressbar.start()

        title, instructions, ingredients = connect.view_requested_recipe(button_id)

        self.view_left_frame = Frame(
            width=self.screen_width, height=self.screen_height / 2
        )
        self.view_left_frame.grid(row=1, column=0, padx=25)

        self.lbl_title = Label(
            self.view_left_frame,
            text=title,
            font=("Arial", 14, "underline"),
            underline=0,
        )
        self.lbl_title.pack()

        self.frame_img = Label(
            self.view_left_frame, image=self.frame_img_list[button_id]
        )
        self.frame_img.image = self.frame_img_list[
            button_id
        ]  # <== anchor to display image
        self.frame_img.pack()

        self.view_right_frame = Frame(
            width=self.screen_width, height=self.screen_height / 2
        )
        self.view_right_frame.grid(row=1, column=1)

        self.lbl_right = Label(
            self.view_right_frame,
            text=f"{title}'s Required Ingredients:",
            font=("bold", 14, "underline"),
            underline=0,
        )
        self.lbl_right.pack()
        self.text = scrolledtext.ScrolledText(
            self.view_right_frame, wrap=WORD, height=10, state="disabled"
        )
        # create the text component
        self.text.pack()
        self.text.configure(state="normal")

        for item in ingredients:
            ingredient = item["original"]
            self.text.insert("end", f"•  {ingredient}\n")
        # disable to stop editing
        self.text.configure(state="disabled")

        self.view_bottom_frame = Frame(
            width=self.screen_width, height=self.screen_height / 3
        )
        self.view_bottom_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.lbl_heading_instructions = Label(
            self.view_bottom_frame,
            text=f"{title}'s Instructions:",
            font=("bold", 14, "underline"),
            underline=0,
        )
        self.lbl_heading_instructions.pack()

        # removes and splits instructions
        instructions_output = self.split_instructions(instructions)

        # Create a Text widget
        self.text_widget = scrolledtext.ScrolledText(
            self.view_bottom_frame, state=NORMAL, wrap=WORD, height=15
        )

        # Insert text into the widget
        for item in instructions_output:
            self.text_widget.insert(END, f"• {item}.\n")

        # Pack the Text widget
        self.text_widget.configure(state=DISABLED)
        self.text_widget.pack()

        self.button_frame = Frame(
            width=self.screen_width, height=self.screen_height / 3
        )
        self.button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        self.btn_main_menu = Button(
            self.button_frame, text="Main Menu!", command=self.main_menu
        )
        self.btn_main_menu.pack(side=LEFT)
        self.btn_quit = Button(
            self.button_frame, text="Quit 0_o", command=self.close_program
        )
        self.btn_quit.pack(side=RIGHT)

        self.progressbar.stop()
        self.progressbar.destroy()
        self.load_frame.destroy()

    def split_instructions(self, instructions):
        """Functions that removes all HTML markup and splits sentences
        *   :returns sentences (__list__)"""
        clean_string = re.sub("<[^<]+?>", "", instructions)
        sentences = re.split("\. ", clean_string)
        return sentences

    def read_recipes(self):
        """Function that gets the title and images of the 6 recipes
        *   :return titles (__list__) images (__list__):"""
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

    def close_program(self):
        """Function that closes the program when the quit button is clicked"""
        self.destroy()

    def main_menu(self):
        """Function that 'reruns' the app by destroying the current one and calling the class object"""
        self.destroy()
        app = AppScreen()
        app.mainloop()


if __name__ == "__main__":
    app = AppScreen()
    app.mainloop()
