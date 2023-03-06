from tkinter import *
import customtkinter
import requests
import components.connect as connect
import io
from PIL import Image, ImageTk
import json

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("J-Cuisine")
        self.geometry(f"{1100}x{600}")

        # call functions
        self.home_screen()

    def home_screen(self):
        """Function that creates all the customTkinter objects for the GUI"""
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)
        # home screen frames
        self.home_frame = customtkinter.CTkFrame(self, width=350, corner_radius=0)
        self.home_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")
        self.home_frame.grid_rowconfigure(5, weight=1)
        self.home_frame.grid_columnconfigure(3, weight=1)

        # home screen main label
        self.home_label = customtkinter.CTkLabel(
            self.home_frame,
            text="Welcome to J-Cuisine!",
            font=customtkinter.CTkFont(size=24, weight="bold"),
        )
        self.home_label.grid(row=0, column=3, padx=20, pady=(20, 10))

        # entry & button label
        self.lookup_label = customtkinter.CTkLabel(
            self.home_frame,
            text="Lookup a recipe for...",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.lookup_label.grid(row=1, column=3)
        # entry field
        self.entry = customtkinter.CTkEntry(
            self.home_frame, width=350, placeholder_text="Lookup recipe"
        )
        self.entry.grid(row=2, column=3, padx=(20, 0), pady=(20, 10))
        # lookup recipes button
        self.lookup_button = customtkinter.CTkButton(
            self.home_frame, text="Lookup", command=self.lookup_recipe
        )
        self.lookup_button.grid(row=3, column=3, padx=20, pady=10)

        # lookup recipe note
        self.note_label = customtkinter.CTkLabel(
            self.home_frame,
            text="*Note that when the field is open that it will give random recipes*",
            font=customtkinter.CTkFont(
                size=12, weight="bold", slant="italic", underline=True
            ),
        )
        self.note_label.grid(row=4, column=3)

    # LOOKUP RECIPE SECTION
    def lookup_recipe(self):
        self.home_frame.destroy()
        self.show_result()

    # SHOW RESULT SECTION
    # VIEW FIRST 6 RECIPES BASED ON USER SEARCH QUERY
    def show_result(self):
        """Function that display the 6 recipes by creating GUI objects"""
        titles, images = self.read_recipes()

        # configure grid layout (3x3) for view recipe
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)

        self.view_frame = customtkinter.CTkFrame(self, width=350, corner_radius=0)
        self.view_frame.grid(row=0, column=0, rowspan=3, columnspan=4, sticky="nsew")
        self.view_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.view_frame.grid_columnconfigure((0, 1, 2), weight=1)

        for i in range(6):
            self.recipe_frame = customtkinter.CTkFrame(self.view_frame, corner_radius=0)
            self.recipe_frame.grid(row=i // 3, column=i % 3, pady=10)

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(images[i], headers=headers)

            # Open the image using PIL
            # recipe_image = Image.open(io.BytesIO(response.content))

            self.recipe_label = customtkinter.CTkLabel(
                self.recipe_frame,
                text=titles[i],
                font=customtkinter.CTkFont(size=14, weight="bold"),
                wraplength=240,
                justify="center",
            )
            self.recipe_label.pack()

            self.tk_image = customtkinter.CTkImage(
                Image.open(io.BytesIO(response.content)),
                size=(330, 220),
            )

            # Convert the PIL image to a Tkinter-compatible format
            # self.tk_image = ImageTk.PhotoImage(recipe_image)

            self.frame_img = customtkinter.CTkLabel(
                self.recipe_frame,
                text="",
                image=self.tk_image,
            )
            self.frame_img.pack()

            self.recipe_button = customtkinter.CTkButton(
                self.recipe_frame,
                text="View Recipe!",
                command=lambda btn_id=i: self.view_recipe(btn_id),
            )
            # self.button_list.append(self.button)
            self.recipe_button.pack(pady=5)

    def view_recipe(self, btn_id):
        print(btn_id)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
