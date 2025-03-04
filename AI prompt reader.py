import dearpygui.dearpygui as dpg
import re


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
    print("Positive prompts:", positive_prompts)
    print("Amount of positive prompts:", len(positive_prompts))
    print(type(positive_prompts))
    print("Negative prompts:", negative_prompts)
    print("Amount of negative prompts:", len(negative_prompts))
    print(type(negative_prompts))

    #3 splitting all prompts by comma
    positive_prompts = positive_prompts.split(",")
    positive_prompts = [prompt.strip() for prompt in positive_prompts if prompt.strip() != ""]
    if negative_prompts:
        negative_prompts = negative_prompts[0].split(",")
    print("Positive prompts:", positive_prompts)
    print("Amount of positive prompts:", len(positive_prompts))
    print(type(positive_prompts))
    print("Negative prompts:", negative_prompts)
    print("Amount of negative prompts:", len(negative_prompts))
    print(type(negative_prompts))

    parse_prompts(positive_prompts, True)
    parse_prompts(negative_prompts, False)

def parse_prompts(prompts, value):
    processed_prompts = []

    # Iterate through each prompt and parse it | Check if it's positive or negative
    for prompt in prompts:
        if value == True:
            prompt_dict = {"Prompt": "", "Emphasis": None, "Weight": None, "Value": "Positive"}
        else:
            prompt_dict = {"Prompt": "", "Emphasis": None, "Weight": None, "Value": "Negative"}
        
        # Check if there is emphasis (((high)))), ((medium)), (low), None
        if prompt.startswith("(((") and prompt.endswith(")))"):
            prompt_dict["Emphasis"] = "High"  
            prompt = prompt[3:-3]  # remove () from prompt

        elif prompt.startswith("((") and prompt.endswith("))"):
            prompt_dict["Emphasis"] = "Medium"  
            prompt = prompt[2:-2]         

        elif prompt.startswith("(") and prompt.endswith(")"):
            prompt_dict["Emphasis"] = "Low"  
            prompt = prompt[1:-1]  

        else:
            prompt_dict["Emphasis"] = None


        # Check if there's weight | :1, :2, :3, :4, :5 etc. float is possible
        weight_match = re.search(r":(\d+)$", prompt)
        if weight_match:
            prompt_dict["Weight"] = int(weight_match.group(1))
            prompt = prompt.replace(f":{weight_match.group(1)}", "")  # Remove weight from prompt
        
       
        prompt_dict["Prompt"] = prompt.strip()  # Clean up any extra spaces and add the prompt to the dictionary
        
        # Add the processed dictionary to the list
        processed_prompts.append(prompt_dict)

    # Display the results
    for prompt in processed_prompts:
        print(prompt)



























# Create the GUI context
dpg.create_context()

# Create a window with an input field and a submit button
with dpg.window(label="AI Prompt Program", width=500, height=400):
    dpg.add_text("Enter your AI prompt:")
    dpg.add_input_text(tag="input_prompt", multiline=True, width=450, height=150)
    dpg.add_button(label="Submit", callback=submit_callback)

# Set up the window's viewport
dpg.create_viewport(title="AI Prompt Program", width=520, height=450)
dpg.setup_dearpygui()
dpg.show_viewport()

# Start the program
dpg.start_dearpygui()

# Clean up after the program exits
dpg.destroy_context()
