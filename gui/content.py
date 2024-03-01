import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class Content:
    def __init__(self, master) -> None:
        self.content_frame = ctk.CTkFrame(master=master)
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(index=0, weight=1)

        self.column_width = 120
        self.scan_result_list(content_frame=self.content_frame)

    def scan_result_list(self, content_frame) -> None:
        title_label = ctk.CTkLabel(
            master=content_frame,
            text="Scan Result",
            font=ctk.CTkFont(family=("JetBrains Mono"), size=33),
            text_color="white",
        )
        title_label.pack(pady=15)

        header_labels: list[str] = [
            "#",
            "IP Address",
            "Protocol",
            "Port",
            "Description",
        ]

        # Scan Result Table
        tree = ttk.Treeview(
            master=content_frame, columns=header_labels, show="headings"
        )
        tree.pack(fill="both", expand=True)

        # Table Styling
        style = ttk.Style()
        style.theme_use(themename="default")
        style.configure(
            style="Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )
        style.map(style="Treeview", background=[("selected", "#22559b")])
        style.configure(
            style="Treeview.Heading",
            background="#565b5e",
            foreground="white",
            relief="flat",
        )
        style.map(style="Treeview.Heading", background=[("active", "#3484F0")])

        # Define Columns
        for col in header_labels:
            tree.heading(column=col, text=col)
            tree.column(column=col, width=self.column_width, anchor="center")

        #! TODO: Replace with actual scan result
        scan_result: list[list[str]] = [
            ["1", "TCP", "69", "KUAY", "OPEN"],
            ["2", "UDP", "420", "HEE", "FILTERED"],
            ["3", "TCP", "55555", "TAD", "OPEN"],
        ]

        # Insert Data
        for item in scan_result:
            tree.insert(parent="", index=tk.END, values=item)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry(geometry_string="1024x768")
    app = Content(master=root)
    root.mainloop()
