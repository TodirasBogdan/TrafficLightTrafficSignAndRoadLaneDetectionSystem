import customtkinter as ctk
from videoplayer import VideoPlayer

video_player = VideoPlayer()

# Create the main window
root = ctk.CTk()
root.title("Traffic Light, Traffic Sign & Road Lane Detection System")
root.iconbitmap("car-icon.ico")
root.geometry("900x600")
heading = ctk.CTkLabel(master=root, text="Traffic Light, Traffic Sign & Road Lane Detection System",
                       font=("Arial", 30), fg_color="transparent", pady=50)
heading.pack()

message_label = ctk.CTkLabel(master=root, text="Please select the options you wish \n to use and choose a file ",
                             font=("Arial", 20), fg_color="transparent")
message_label.place(x=450, y=200)

file_text_label = ctk.CTkLabel(master=root, text="File:",
                               font=("Arial", 11), fg_color="transparent")
file_text_label.place(x=600, y=320)

file_path_label = ctk.CTkLabel(master=root, text="",
                               font=("Arial", 11), fg_color="transparent")
file_path_label.place(x=450, y=350)

# Create a traffic light detection switch
var_traffic_light = ctk.StringVar()
switch_button_traffic_light = ctk.CTkSwitch(master=root, text="Traffic Light",
                                            variable=var_traffic_light,
                                            onvalue="on", offvalue="off",
                                            font=("Arial", 20))
switch_button_traffic_light.place(x=50, y=150)

# Create a traffic sign detection switch
var_traffic_sign = ctk.StringVar()
switch_button_traffic_sign = ctk.CTkSwitch(master=root, text="Traffic Sign",
                                           variable=var_traffic_sign,
                                           onvalue="on", offvalue="off",
                                           font=("Arial", 20))
switch_button_traffic_sign.place(x=50, y=200)

# Create a road lane line detection switch
var_road_lane = ctk.StringVar()
switch_button_road_lane = ctk.CTkSwitch(master=root, text="Road Lane Lines",
                                        variable=var_road_lane,
                                        onvalue="on", offvalue="off",
                                        font=("Arial", 20))
switch_button_road_lane.place(x=50, y=250)


# Create a resize slider event
def slider_resize_video_event(value):
    slider_resize_video_label_percentage.configure(text=str(value) + "%")


# Create a resize slider
slider_resize_video = ctk.CTkSlider(root, from_=10, to=190, orientation="horizontal", border_width=5,
                                    command=slider_resize_video_event)
slider_resize_video.place(x=50, y=350)

# Create a resize slider text label
slider_resize_video_label_text = ctk.CTkLabel(master=root, text="Resize video",
                                              font=("Arial", 20), fg_color="transparent")
slider_resize_video_label_text.place(x=50, y=300)
# Create a resize slider percentage label
slider_resize_video_label_percentage = ctk.CTkLabel(master=root, text=str(slider_resize_video.get()) + "%",
                                                    font=("Arial", 15), fg_color="transparent")
slider_resize_video_label_percentage.place(x=200, y=300)


# Create a confidence slider event
def slider_confidence_event(value):
    slider_confidence_label_percentage.configure(text=str(value) + "%")


# Create a confidence slider
slider_confidence = ctk.CTkSlider(root, from_=0, to=100, orientation="horizontal", border_width=5,
                                  command=slider_confidence_event)
slider_confidence.place(x=50, y=450)

# Create a confidence slider text label
slider_confidence_label_text = ctk.CTkLabel(master=root, text="Prediction Confidence",
                                            font=("Arial", 20), fg_color="transparent")
slider_confidence_label_text.place(x=50, y=400)
# Create a confidence slider percentage label
slider_confidence_label_percentage = ctk.CTkLabel(master=root, text=str(slider_confidence.get()) + "%",
                                                  font=("Arial", 15), fg_color="transparent")
slider_confidence_label_percentage.place(x=275, y=400)


# Create a browse button event
def browse_button_event():
    file_path = video_player.open_file()
    message_label.configure(text="Now press Start\nPress q to exit prediction page")
    file_path_label.configure(text=file_path)


# Create a browse button
browse_button = ctk.CTkButton(root, text="Choose File",
                              command=lambda: browse_button_event(),
                              width=100, height=50, corner_radius=11, font=("Arial", 16))
browse_button.place(x=400, y=500)

# Create a play button
start_button = ctk.CTkButton(root, text="Start",
                             command=lambda: video_player.play_video(traffic_light=var_traffic_light.get(),
                                                                     traffic_sign=var_traffic_sign.get(),
                                                                     road_lane=var_road_lane.get(),
                                                                     rescale_percent=slider_resize_video.get(),
                                                                     confidence=slider_confidence.get() / 100),
                             width=100, height=50, corner_radius=11, font=("Arial", 16))
start_button.place(x=700, y=500)

# Keep the main window active
root.mainloop()
