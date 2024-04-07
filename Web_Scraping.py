from tkinter import filedialog
from tkinter import ttk
import datetime
import customtkinter as ctk

from web_scrpit import web_scraping_books as wb


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder_label.config(text="Selected Folder: " + folder_path)


def confirm_and_scrape():
    if folder_path:
        confirm_label.config(text="Scraping and saving...")
        save_path = folder_path + f"/travel_books{datetime.date.today().strftime('%Y-%m-%d')}.csv"
        wb(save_path)
        status_label.config(text="Books scraped and saved successfully!")
    else:
        confirm_label.config(text="Please select a folder first.")


def main():
    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")
    window = ctk.CTk()
    window.title("Book Scraper")
    window.geometry("400x250")

    website_label = ttk.Label(window, text="Website: books.toscrape.com")
    website_label.pack(pady=10)

    select_folder_button = ttk.Button(window, text="Select Folder", command=select_folder)
    select_folder_button.pack(pady=5)

    global selected_folder_label
    selected_folder_label = ttk.Label(window, text="")
    selected_folder_label.pack()

    confirm_button = ttk.Button(window, text="Confirm and Scrape", command=confirm_and_scrape)
    confirm_button.pack(pady=5)

    global confirm_label
    confirm_label = ttk.Label(window, text="")
    confirm_label.pack()

    global status_label
    status_label = ttk.Label(window, text="")
    status_label.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
