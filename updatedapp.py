from tkinter import *
import customtkinter

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
        self.geometry(f"{1100}x{580}")

        # configure grid layout (3x2) for view recipe
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

        self.lookup_label = customtkinter.CTkLabel(
            self.home_frame,
            text="Lookup a recipe for...",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.lookup_label.grid(row=1, column=3)

        self.entry = customtkinter.CTkEntry(
            self.home_frame, width=350, placeholder_text="Lookup recipe"
        )
        self.entry.grid(row=2, column=3, padx=(20, 0), pady=(20, 10))
        self.lookup_button = customtkinter.CTkButton(
            self.home_frame, text="Lookup", command=""
        )
        self.lookup_button.grid(row=3, column=3, padx=20, pady=10)
        self.note_label = customtkinter.CTkLabel(
            self.home_frame,
            text="*Note that when the field is open that it will give random recipes*",
            font=customtkinter.CTkFont(
                size=12, weight="bold", slant="italic", underline=True
            ),
        )
        self.note_label.grid(row=4, column=3)


if __name__ == "__main__":
    app = App()
    app.mainloop()
