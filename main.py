from tkinter import messagebox
from tkinter.ttk import Treeview, Scrollbar, Style
from ttkwidgets import CheckboxTreeview
import json
from customtkinter import (
    CTk,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkButton,
    CTkComboBox,
    CTkCheckBox,
    CTkRadioButton,
    StringVar,
    IntVar,
)
from utils import interface, scanner, probe


def probe_update():
    json_set = probe.get_ip_subset(
        interface_info=network_interface_json,
        interface_name=select_interface.get(),
        subset_no=16,
    )
    ip_address_treeview.delete(*ip_address_treeview.get_children())
    ip_address_treeview.insert(
        parent="", index="end", iid=0, text="127.0.0.1", tags=("unchecked")
    )
    ip_address_treeview.update()

    j = 1
    for subset in json_set["subset"]:
        probe_result = probe.probe_subset(subset=subset)
        for res in probe_result["addr_set"]:
            ip_address_treeview.insert(
                parent="", index="end", iid=j, text=res, tags=("unchecked")
            )
            ip_address_treeview.update()
            j += 1


def insert_ipaddr():
    member = ip_address_treeview.get_children()
    value = ip_address_entry.get()
    value_json = json.dumps({"name": select_interface.get(), "addr_set": [value]})

    result = probe.probe_subset(subset=json.loads(value_json))
    if result is None:
        messagebox.showinfo(title="Error", message=f"{value} not found")
        return

    n = member.__len__()
    ip_address_treeview.insert(
        parent="",
        index="end",
        iid=n + 1,
        text=result["addr_set"][0],
        tags=("unchecked"),
    )


def scan():
    checked_iter = ip_address_treeview.get_checked()

    mode = scan_mode_var.get()
    if mode == 1:
        mode_str = "fast"
    elif mode == 2:
        mode_str = "full"
    else:
        mode_str = "No"

    for checked in checked_iter:
        check_ip = ip_address_treeview.item(item=checked)["text"]
        result_json = scanner.tcp_scan(ipaddr=check_ip, mode=mode_str)


app = CTk()
app.geometry(geometry_string="960x720")
app.resizable(width=False, height=False)
app.title(string="Network Scanner Tool with Rust")

left_frame = CTkFrame(
    master=app,
    width=320,
    height=720,
    bg_color="#123456",
    fg_color="#123456",
    corner_radius=0,
    border_width=0,
)
left_frame.pack(side="left", fill="both", expand=True)

ip_address_section = CTkFrame(
    master=left_frame, bg_color="transparent", fg_color="#123456"
)
ip_address_section.pack()

ip_address_label = CTkLabel(
    master=ip_address_section,
    text="IP Address:",
    font=("JetBrains Mono", 13, "bold"),
)
ip_address_label.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="w")

ip_address_entry = CTkEntry(
    master=ip_address_section,
    placeholder_text="Enter IP Address...",
    font=("JetBrains Mono", 11, "bold"),
    width=150,
    height=30,
)
ip_address_entry.grid(row=1, column=0, padx=5, pady=0)

add_ip_button = CTkButton(
    master=ip_address_section,
    text="Add IP Address",
    font=("JetBrains Mono", 12, "bold"),
    width=120,
    height=30,
    corner_radius=15,
    fg_color="#6B9FDC",
    command=lambda: insert_ipaddr(),
)
add_ip_button.grid(row=1, column=1, padx=5)

network_interface_section = CTkFrame(
    master=left_frame, bg_color="transparent", fg_color="#123456"
)
network_interface_section.pack()

network_interface_label = CTkLabel(
    master=network_interface_section,
    text="Network Interface:",
    font=("JetBrains Mono", 13, "bold"),
)
network_interface_label.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="w")

network_interface_json = interface.interface_info()
network_interfaces: list[str] = interface.get_interfaces_name()
select_interface = StringVar(value=network_interfaces[0])
network_interface_dropdown = CTkComboBox(
    master=network_interface_section,
    values=network_interfaces,
    width=150,
    height=30,
    font=("JetBrains Mono", 11),
    dropdown_font=("JetBrains Mono", 13),
    state="readonly",
    variable=StringVar(value=network_interfaces[0]),
)
network_interface_dropdown.grid(row=1, column=0, padx=5, pady=0)

probe_button = CTkButton(
    master=network_interface_section,
    text="Probe",
    font=("JetBrains Mono", 12, "bold"),
    width=120,
    height=30,
    corner_radius=15,
    fg_color="#A469C4",
    hover_color="#8069C4",
    command=lambda: probe_update(),
)
probe_button.grid(row=1, column=1, padx=5)

ip_address_list_frame = CTkFrame(
    master=left_frame, bg_color="transparent", fg_color="#123456"
)
ip_address_list_frame.pack()

ip_address_list_label = CTkLabel(
    master=ip_address_list_frame,
    text="IP Address List",
    font=("JetBrains Mono", 16, "bold"),
    anchor="center",
    compound="center",
)
ip_address_list_label.grid(row=0, column=0, columnspan=2, pady=(30, 0), sticky="nsew")

ip_address_treeview = CheckboxTreeview(
    master=ip_address_list_frame,
    show="tree",  # hide tree headings
)
ip_address_treeview.grid(row=1, column=0, columnspan=2, pady=(5, 0))

ip_address_list_scrollbar = Scrollbar(
    master=ip_address_list_frame,
    orient="vertical",
    command=ip_address_treeview.yview,
    style="TScrollbar",
    cursor="arrow",
)
ip_address_treeview.configure(yscroll=ip_address_list_scrollbar.set)
ip_address_list_scrollbar.grid(row=1, column=2, padx=0, pady=(5, 0), sticky="ns")

ip_addresses: list[str] = ["127.0.0.1"]

for index, ip_address in enumerate(iterable=ip_addresses):
    ip_address_treeview.insert(
        parent="", index="end", iid=index, text=ip_address, tags=("unchecked",)
    )

ip_address_check_all_button = CTkButton(
    master=ip_address_list_frame,
    text="Select All",
    bg_color="transparent",
    width=100,
    height=25,
    command=lambda: print("select all"),
)
ip_address_check_all_button.grid(row=2, column=0, padx=5, pady=5)

ip_address_uncheck_all_button = CTkButton(
    master=ip_address_list_frame,
    text="Unselect All",
    bg_color="transparent",
    fg_color="#CD6464",
    width=100,
    height=25,
    command=lambda: print("unselect all"),
)
ip_address_uncheck_all_button.grid(row=2, column=1, padx=5, pady=5)

scan_option_frame = CTkFrame(
    master=left_frame, bg_color="transparent", fg_color="#123456"
)
scan_option_frame.pack()
scan_option_frame.columnconfigure(index=0, weight=2)

scan_option_label = CTkLabel(
    master=scan_option_frame,
    text="Scan Option",
    font=("JetBrains Mono", 16, "bold"),
)
scan_option_label.grid(row=0, column=0, columnspan=2, pady=(25, 0), sticky="nsew")

scan_option_protocol_label = CTkLabel(
    master=scan_option_frame,
    text="Protocol:",
    font=("JetBrains Mono", 13, "bold"),
)
scan_option_protocol_label.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")

scan_protocol_tcp = CTkCheckBox(
    master=scan_option_frame,
    text="TCP",
    font=("JetBrains Mono", 12, "bold"),
)
scan_protocol_tcp.grid(row=2, column=0, padx=5, pady=5)

scan_protocol_udp = CTkCheckBox(
    master=scan_option_frame,
    text="UDP",
    font=("JetBrains Mono", 12, "bold"),
)
scan_protocol_udp.grid(row=3, column=0, padx=5, pady=5)

scan_option_mode_label = CTkLabel(
    master=scan_option_frame,
    text="Scan Mode:",
    font=("JetBrains Mono", 13, "bold"),
)
scan_option_mode_label.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")

scan_mode_var = IntVar()
scan_mode_fast = CTkRadioButton(
    master=scan_option_frame,
    text="Fast",
    font=("JetBrains Mono", 12, "bold"),
    variable=scan_mode_var,
    value=1,
)
scan_mode_fast.grid(row=2, column=1, padx=5, pady=5)
scan_mode_fast.select()

scan_mode_full = CTkRadioButton(
    master=scan_option_frame,
    text="Full",
    font=("JetBrains Mono", 12, "bold"),
    variable=scan_mode_var,
    value=2,
)
scan_mode_full.grid(row=3, column=1, padx=5, pady=5)

scan_button = CTkButton(
    master=scan_option_frame,
    text="Scan",
    text_color="#000000",
    font=("JetBrains Mono", 21, "bold"),
    width=150,
    height=50,
    corner_radius=25,
    bg_color="transparent",
    fg_color="#FEDCBA",
    command=lambda: scan(),
)
scan_button.grid(row=4, column=0, columnspan=2, padx=5, pady=15, sticky="nsew")


right_frame = CTkFrame(
    master=app,
    width=640,
    height=720,
    bg_color="#E3E3E3",
    fg_color="#E3E3E3",
)
right_frame.pack(side="right", fill="both", expand=True)

top_frame = CTkFrame(
    master=right_frame,
    width=640,
    height=60,
    bg_color="#ABCDEF",
    fg_color="#ABCDEF",
    corner_radius=0,
)
top_frame.pack(side="top", fill="x")

top_label = CTkLabel(
    master=top_frame,
    text="Scan Result",
    text_color="#000000",
    font=("JetBrains Mono", 25, "bold"),
)
top_label.pack(pady=10, padx=10, anchor="center")

scan_result_frame = CTkFrame(
    master=right_frame,
    width=620,
    height=500,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    corner_radius=0,
)
scan_result_frame.pack(pady=25, padx=0, anchor="center")

treeview_style = Style()
treeview_style.configure(
    style="Treeview",
    font=("JetBrains Mono", 9),
    rowheight=25,
)

scan_result_tree_columns = ("ip_address", "protocol", "description", "status")
scan_result_tree = Treeview(
    master=scan_result_frame,
    columns=scan_result_tree_columns,
    show="headings",
    style="Treeview",
)

scan_result_tree.column(column="ip_address", width=100, minwidth=100)
scan_result_tree.column(column="protocol", width=60, minwidth=60)
scan_result_tree.column(column="description", width=270, minwidth=270)
scan_result_tree.column(column="status", width=80, minwidth=80)

scan_result_tree.heading(column="ip_address", text="IP Address", anchor="w")
scan_result_tree.heading(column="protocol", text="Protocol", anchor="w")
scan_result_tree.heading(column="description", text="Description", anchor="w")
scan_result_tree.heading(column="status", text="Status", anchor="w")


def item_selected(event):
    for selected_item in scan_result_tree.selection():
        item = scan_result_tree.item(item=selected_item)
        record = item["values"]
        messagebox.showinfo(title="Scan Result", message=", ".join(record))


scan_result_tree.bind("<<TreeviewSelect>>", func=item_selected)
scan_result_tree.grid(row=0, column=0, sticky="nsew")

scrollbar = Scrollbar(
    master=scan_result_frame,
    orient="vertical",
    command=scan_result_tree.yview,
    style="TScrollbar",
    cursor="arrow",
)
scan_result_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

scan_results = []
for scan_result in scan_results:
    scan_result_tree.insert(parent="", index="end", values=scan_result)


bottom_frame = CTkFrame(
    master=right_frame,
    width=640,
    height=90,
    bg_color="#ABCDEF",
    fg_color="#ABCDEF",
    corner_radius=0,
)
bottom_frame.pack(side="bottom", fill="x")

stop_button = CTkButton(
    master=bottom_frame,
    text="Stop",
    text_color="#000000",
    font=("JetBrains Mono", 25, "bold"),
    bg_color="transparent",
    fg_color="#CD6464",
    corner_radius=50,
    command=lambda: print("scan stopped!"),
)
stop_button.pack(pady=10, padx=10, anchor="center")


app.mainloop()
