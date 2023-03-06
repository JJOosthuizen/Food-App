from tkinter import *
import customtkinter
import requests
import components.connect as connect
import io
from PIL import Image
import json
import re

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

        self.image_list = []
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
            recipe_img = Image.open(io.BytesIO(response.content))
            self.tk_image = customtkinter.CTkImage(recipe_img, size=(330, 220))

            self.image_list.append(recipe_img)

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
        self.view_frame.destroy()

        self.detail_frame = customtkinter.CTkFrame(self, width=350, corner_radius=0)
        self.detail_frame.grid(row=0, column=0, rowspan=5, columnspan=4, sticky="nsew")
        self.detail_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        self.detail_frame.grid_columnconfigure((0, 1, 2), weight=1)

        title, instructions, ingredients = connect.view_requested_recipe(btn_id)

        # TOP LEFT SIDE
        self.lbl_title = customtkinter.CTkLabel(
            self.detail_frame,
            text=title,
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.lbl_title.grid(row=0, column=0)

        food_img = customtkinter.CTkImage(self.image_list[btn_id], size=(330, 220))
        self.detail_img = customtkinter.CTkLabel(
            self.detail_frame, text="", image=food_img
        )

        self.detail_img.grid(row=1, column=0, pady=10)

        # TOP RIGHT SIDE
        self.lbl_ingredients = customtkinter.CTkLabel(
            self.detail_frame,
            text=f"{title}'s Required Ingredients:",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.lbl_ingredients.grid(row=0, column=1, columnspan=2)

        self.ingredient_textbox = customtkinter.CTkTextbox(
            self.detail_frame, width=300, font=customtkinter.CTkFont(size=14)
        )
        self.ingredient_textbox.grid(
            row=1, column=1, columnspan=2, padx=40, pady=10, sticky="nsew"
        )

        for item in ingredients:
            ingredient = item["original"]
            self.ingredient_textbox.insert("end", f"•  {ingredient}\n")
        # disable to stop editing
        self.ingredient_textbox.configure(state="disabled")

        # BOTTOM SIDE
        self.lbl_instructions = customtkinter.CTkLabel(
            self.detail_frame,
            text=f"{title}'s Instructions:",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.lbl_instructions.grid(row=3, column=0, columnspan=3, pady=(15, 0))

        # removes and splits instructions
        instructions_output = self.split_instructions(instructions)

        # Create a Text widget
        self.instructions_textbox = customtkinter.CTkTextbox(
            self.detail_frame, width=300, font=customtkinter.CTkFont(size=16)
        )
        self.instructions_textbox.grid(
            row=4, column=0, columnspan=3, padx=40, pady=20, sticky="nsew"
        )

        # Insert text into the widget
        for item in instructions_output:
            self.instructions_textbox.insert(END, f"• {item}.\n")

        # Pack the Text widget
        self.instructions_textbox.configure(state="disabled")

        # Buttons
        # change color theme selection
        self.theme_button = customtkinter.CTkButton(
            self.detail_frame, text="", command=self.lookup_recipe
        )
        self.theme_button.grid(row=5, column=0, padx=20, pady=10)
        # main menu button
        self.main_menu_button = customtkinter.CTkButton(
            self.detail_frame, text="Main Menu", command=self.main_menu
        )
        self.main_menu_button.grid(row=5, column=1, padx=20, pady=10)

        # Quit button
        self.quit_button = customtkinter.CTkButton(
            self.detail_frame, text="Quit 0_o", command=self.close_program
        )
        self.quit_button.grid(row=5, column=2, padx=20, pady=10)

    def split_instructions(self, instructions):
        """Functions that removes all HTML markup and splits sentences
        *   :returns sentences (__list__)"""
        clean_string = re.sub("<[^<]+?>", "", instructions)
        sentences = re.split("\. ", clean_string)
        return sentences

    def close_program(self):
        """Function that closes the program when the quit button is clicked"""
        self.destroy()

    def main_menu(self):
        """Function that 'reruns' the app by destroying the current one and calling the class object"""
        self.destroy()
        app = App()
        app.mainloop()

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
