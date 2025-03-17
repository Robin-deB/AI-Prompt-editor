import dearpygui.dearpygui as dpg
import re
row_counter = 1

def submit_callback(): # this function gets the input value and splits it in prompts
    user_input = dpg.get_value("input_prompt") 
    print("User input:", user_input) 
    process_prompt(user_input) # call the function to process the prompt

def process_prompt(user_input): # this function processes the prompt by first dividing it negative and positive prompts
    # 1. Split out negative prompts by []
    negative_prompts = re.findall(r'\[(.*)\]', user_input)

    # 2. Remove negative prompts from the user input and create positive prompts list
    user_input = re.sub(r'\[(.*)\]', '', user_input)
    positive_prompts = user_input

    #debug info
    print("Positive prompts:", positive_prompts)
    print("Amount of positive prompts:", len(positive_prompts))
    print(type(positive_prompts))
    print("Negative prompts:", negative_prompts)
    print("Amount of negative prompts:", len(negative_prompts))
    print(type(negative_prompts))

    #3 splitting all prompts by comma and cleaning up extra spaces
    positive_prompts = positive_prompts.split(",")
    positive_prompts = [prompt.strip() for prompt in positive_prompts if prompt.strip() != ""]
    if negative_prompts:
        negative_prompts = negative_prompts[0].split(",")

    #debug info
    print("Positive prompts:", positive_prompts)
    print("Amount of positive prompts:", len(positive_prompts))
    print(type(positive_prompts))
    print("Negative prompts:", negative_prompts)
    print("Amount of negative prompts:", len(negative_prompts))
    print(type(negative_prompts))


    #4 parse the prompts (seperate function)
    parse_prompts(positive_prompts, True)
    parse_prompts(negative_prompts, False)

def parse_prompts(prompts, value):
    processed_prompts = []

    # Iterate through each prompt and parse it | Check if it's positive or negative | also set up dictionary lay out for each prompt
    for prompt in prompts:
        if value == True:
            prompt_dict = {"Prompt": "", "Emphasis": None, "Weight": None, "Value": "Positive"}
        else:
            prompt_dict = {"Prompt": "", "Emphasis": None, "Weight": None, "Value": "Negative"}
        
        # Check if there is emphasis (((high)))), ((medium)), (low), None
        if prompt.startswith("(((") and prompt.endswith(")))"):
            prompt_dict["Emphasis"] = "High"  
            prompt = prompt[3:-3]  # remove ()s from prompt

        elif prompt.startswith("((") and prompt.endswith("))"):
            prompt_dict["Emphasis"] = "Medium"  
            prompt = prompt[2:-2]         

        elif prompt.startswith("(") and prompt.endswith(")"):
            prompt_dict["Emphasis"] = "Low"  
            prompt = prompt[1:-1]  

        else:
            prompt_dict["Emphasis"] = None


        # Check if there's weight | :1, :2, :3, :4, :5 etc. float is possible, negative float is also possible
        weight_match = re.search(r":(\d+)$", prompt)
        if weight_match:
            prompt_dict["Weight"] = int(weight_match.group(1))
            prompt = prompt.replace(f":{weight_match.group(1)}", "")  # Remove weight from prompt
        
       
        prompt_dict["Prompt"] = prompt.strip()  # Clean up any extra spaces and add the prompt to the dictionary
        
        # Add the processed dictionary to the list
        processed_prompts.append(prompt_dict)

    # visualizes the prompts&values in a grid that allows to change it
    add_grid(processed_prompts)

    #debug info
    for prompt in processed_prompts:
        print(prompt)
        print(type(prompt))
        print()
        print(processed_prompts)
        print(type(processed_prompts))

def add_grid(processed_prompts): # this function adds the prompts to the grid
    global row_counter
    for i in range(len(processed_prompts)): # iterate through the prompts in the list and extracts its values
        prompt = str(processed_prompts[i].get('Prompt'))
        emphasis =processed_prompts[i].get('Emphasis')
        weight = processed_prompts[i].get('Weight')	
        if weight == None: #changes None into float 0.0
            weight = 0.0
        weight_float = float(weight)

        # creates the grid with input fields
        with dpg.group(parent=AI_parsed_group, horizontal=True, tag=f"row_{row_counter}", horizontal_spacing=10):
            dpg.add_text(f"{row_counter}") #row counter, also shows the priority of the prompt (earlier prompts higher priority)
            dpg.add_input_text(default_value=f"{prompt}", indent=20,width=450) #input field of the prompt. Open string
            dpg.add_combo(("High", "Medium", "Low", "None"), default_value=emphasis, width=80) #combo box of the emphasis. High, Medium, Low, None
            dpg.add_input_float(format="%.02f", default_value=weight_float, width=100) #input field of the weight in float format
        row_counter += 1 #ensures after every prompt the row counter is added up.


#Create the GUI context
dpg.create_context()

#Create a window with an input field and a submit button
with dpg.window(label="AI Prompt Program", width=1280, height=720): #setup the window
    with dpg.group(horizontal=True, tag="main"): #ensures the prompt window and grid are horizontal/next to each other
        with dpg.group(horizontal=False, tag="promptfield"):
            dpg.add_text("Enter your AI prompt:")
            dpg.add_input_text(tag="input_prompt", multiline=True, width=450, height=150)
            with dpg.group(horizontal=True, tag="promptfieldbuttons"):  
                dpg.add_button(label="Submit", callback=submit_callback)
                dpg.add_button(label="Text", callback=print("Text"))
        with dpg.group(horizontal=False, tag="gridfield"):
            with dpg.group(label="header", horizontal=True):
                # Centered headers using indent approach
                with dpg.group(horizontal=True, width=400, tag="header_prompt"):
                    dpg.add_text("Prompt", indent=30,)  # Adjust the indent to center
                with dpg.group(horizontal=True, width=150, tag="header_emphasis"):
                    dpg.add_text("Emphasis", indent=400)  # Adjust the indent to center
                with dpg.group(horizontal=True, width=150, tag="header_weight"):
                    dpg.add_text("Weight", indent=30)  # Adjust the indent to center
            
            # The AI_parsed_group where rows are dynamically added
            with dpg.group(horizontal=False, tag="AI_parsed_group") as AI_parsed_group:
                pass

        

# Set up the window's viewport
dpg.create_viewport(title="AI Prompt Program", width=1280, height=720)
dpg.setup_dearpygui()
dpg.show_viewport()

# Start the program
dpg.start_dearpygui()

# Clean up after the program exits
dpg.destroy_context()


