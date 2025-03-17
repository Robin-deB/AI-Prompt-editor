import dearpygui.dearpygui as dpg
import re
import time
import asyncio

pos_row_counter = 1
neg_row_counter = 1
positive_prompts = []
negative_prompts = []

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def add_prompt(prompt, emphasis, weight, value): # this function adds the prompts to the grid
    global pos_row_counter
    global neg_row_counter


    if value == "Positive":
        # creates the grid with input fields
        with dpg.group(parent=AI_parsed_group_pos, horizontal=True, horizontal_spacing=10):
            dpg.add_text(f"{pos_row_counter}") #row counter, also shows the priority of the prompt (earlier prompts higher priority)
            dpg.add_input_text(default_value=f"{prompt}", indent=20,width=450) #input field of the prompt. Open string
            dpg.add_combo(("High", "Medium", "Low", "None"), default_value=emphasis, width=80) #combo box of the emphasis. High, Medium, Low, None
            dpg.add_input_float(format="%.02f", default_value=weight, width=100) #input field of the weight in float format             
            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Up)
            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Down)
            dpg.add_button(label="X")
        pos_row_counter += 1 #ensures after every prompt the row counter is added up.

    else:
        # creates the grid with input fields
        with dpg.group(parent=AI_parsed_group_neg, horizontal=True, horizontal_spacing=10):
            dpg.add_text(f"{neg_row_counter}") #row counter, also shows the priority of the prompt (earlier prompts higher priority)
            dpg.add_input_text(default_value=f"{prompt}", indent=20,width=450) #input field of the prompt. Open string
            dpg.add_combo(("High", "Medium", "Low", "None"), default_value=emphasis, width=80) #combo box of the emphasis. High, Medium, Low, None
            dpg.add_input_float(format="%.02f", default_value=weight, width=100) #input field of the weight in float format             
            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Up)
            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Down)
            dpg.add_button(label="X", callback=lambda: dpg.delete_item(f"row_{neg_row_counter}"))
        neg_row_counter += 1 #ensures after every prompt the row counter is added up.

    reset_modal()#resets the modal values

def submit_prompt(prompt, emphasis, weight, value):
    print(prompt, emphasis, weight, value)
    prompt_dict = {"Prompt": "", "Emphasis": None, "Weight": None, "Value": "Positive"}
    prompt_dict["Prompt"] = prompt
    prompt_dict["Emphasis"] = emphasis
    prompt_dict["Weight"] = weight
    prompt_dict["Value"] = value
    if value == "Positive":
        positive_prompts.append(prompt_dict)
    else:
        negative_prompts.append(prompt_dict)
    
    add_prompt(prompt, emphasis, weight, value)

def center_modal():
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    
    window_width = 400  # Adjust based on modal size
    window_height = 200
    
    x_pos = (viewport_width - window_width) // 2
    y_pos = (viewport_height - window_height) // 2
    
    dpg.set_item_pos("modal_window", [x_pos, y_pos])

def open_modal():
    center_modal()  # Center before showing
    dpg.configure_item("modal_window", show=True)

def reset_modal(): #resets the modal values
    dpg.set_value(modal_prompt, "")
    dpg.set_value(modal_emphasis, "None")
    dpg.set_value(modal_weight, 0.0)
    dpg.set_value(modal_value, "Positive")


async def show_popup():
    dpg.configure_item("warning_popup", show=True)
    await asyncio.sleep(1)
    dpg.configure_item("warning_popup", show=False)

def check_input_prompt(prompt):
    if prompt == "":
        asyncio.run(show_popup())
        return
    else:
        emphasis = dpg.get_value("modalemphasis")
        weight = dpg.get_value("modalweight")
        value = dpg.get_value("modalvalue")
        submit_prompt(prompt, emphasis, weight, value)
        dpg.configure_item("modal_window", show=False)



#Create the GUI context
dpg.create_context()




#Prompt Modal used for adding prompts to the list.
with dpg.window(label="Prompt maker", tag="modal_window", width=550, height=200, modal=True, show=False):
    dpg.add_spacer(height=5)

    modal_prompt = dpg.add_input_text(width=500, height=20) #input field of the prompt. Open string
    
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        modal_emphasis = dpg.add_combo(("High", "Medium", "Low", "None"),label="Emphasis", tag="modalemphasis", default_value="None", width=80) #combo box of the emphasis. High, Medium, Low, None
        with dpg.popup(tag="__demo_popup1"):
            dpg.add_spacer(width=10)
        modal_weight = dpg.add_input_float(label="Weight", tag="modalweight", format="%.02f", default_value=float(0), max_value=10.0, min_value=-10.0, width=100) #input field of the weight in float format
    
    dpg.add_spacer(height=5)      
    
    with dpg.group(horizontal=True):
        dpg.add_text("Prompt Type:")
        dpg.add_spacer(width=10)        
        modal_value = dpg.add_radio_button(("Positive", "Negative"),tag="modalvalue", default_value="Positive", horizontal=True)  #radio button of the prompt type. Positive, Negative.

    dpg.add_spacer(height=40)

    with dpg.group(horizontal=True):#first button is submit, calls function (submitprompt while extracting all input values), second button is close
        dpg.add_button(label="Submit", width=80, height=20, callback=lambda: (check_input_prompt(dpg.get_value(modal_prompt))))
        dpg.add_spacer(width=270)
        dpg.add_button(label="Close", width=80, height=20, callback=lambda: dpg.configure_item("modal_window", show=False))

#Main screen
with dpg.window(label="AI Prompt Maker", width=1920, height=1080): #setup the window
       
    dpg.add_button(label="Add Prompt", callback=open_modal)
    
    dpg.add_separator()
    with dpg.group(horizontal=True, tag="Main"):
#grid for the positive prompts
        with dpg.group(horizontal=False, tag="Positive_Prompts"):
            dpg.add_text("Positive Prompts") 
            with dpg.group(label="header", horizontal=True):
                with dpg.group(horizontal=True, width=400, tag="header_prompt_pos"):
                    dpg.add_text("Prompt", indent=30,)  
                with dpg.group(horizontal=True, width=150, tag="header_emphasis_pos"):
                    dpg.add_text("Emphasis", indent=400) 
                with dpg.group(horizontal=True, width=150, tag="header_weight_pos"):
                    dpg.add_text("Weight", indent=30)
                dpg.add_spacer(width=130)                 
            with dpg.group(horizontal=False, tag="AI_parsed_group_+") as AI_parsed_group_pos:
                pass

        with dpg.drawlist(width=10, height=1200): #vertical separator for easy reading
            dpg.draw_line((5, 0), (5, 1500), color=(150, 150, 150, 255), thickness=1)

#grid for the negative prompts
        with dpg.group(horizontal=False, tag="Negative_Prompts"):
            dpg.add_text("Negative Prompts") 
            with dpg.group(label="header", horizontal=True):
                with dpg.group(horizontal=True, width=400, tag="header_prompt_neg"):
                    dpg.add_text("Prompt", indent=30,)  
                with dpg.group(horizontal=True, width=150, tag="header_emphasis_neg"):
                    dpg.add_text("Emphasis", indent=400) 
                with dpg.group(horizontal=True, width=150, tag="header_weight_neg"):
                    dpg.add_text("Weight", indent=30) 
            with dpg.group(horizontal=False, tag="AI_parsed_group_-") as AI_parsed_group_neg:
                pass
        # Ensure the modal stays centered when resizing
def on_viewport_resize():
    if dpg.is_item_shown("modal_window"):
        center_modal()

dpg.set_viewport_resize_callback(on_viewport_resize)



dpg.create_viewport(title="AI Prompt Maker", width=1280, height=720)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()