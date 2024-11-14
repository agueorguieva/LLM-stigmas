import torch
import pandas as pd
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
from helper_functions import stigmas_list, averaged_values, concealability_classification, course_classification, disruptiveness_classification, aesthetics_classification, origin_classification, peril_classification, extract_value


torch.cuda.empty_cache() #managing GPU cache

#access to Mistral transformers requires approval of terms and conditions
from huggingface_hub import login, logout
login("hf_XXXXXX") 

#import model
mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer_m = AutoTokenizer.from_pretrained(mistral_model)
model_m = AutoModelForCausalLM.from_pretrained(mistral_model, torch_dtype=torch.float16, device_map="auto")


def run_mistral(prompt):
    
    #im not sure if i need this .eval()
   # model_m.eval()

    chat = [
        { "role": "user", "content": prompt, "temperature" : 0.2},
    ]
    chat = tokenizer_m.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    # tokenize the text
    input_tokens = tokenizer_m(chat, return_tensors="pt").to(model_m.device)
    # generate output tokens
    output = model_m.generate(**input_tokens, 
                              do_sample = True,
                        max_new_tokens=100)
    # decode output tokens into text
    output = tokenizer_m.batch_decode(output)
  
    #clean output to be just the number, unsure, or improper value
    cleaned_output = extract_value(str(output), 'mistral')

    return cleaned_output

def generate_all_data(stigmas, iterations):

    visibilities = {k:[] for k in stigmas}
    course = {k:[] for k in stigmas}
    disrupt = {k:[] for k in stigmas}
    aesthetics = {k:[] for k in stigmas}
    origin = {k:[] for k in stigmas}
    peril = {k:[] for k in stigmas}


    for stigma in stigmas:
        for i in range(0,iterations):
            visibilities[stigma].append(run_mistral(concealability_classification(stigma)))
            course[stigma].append(run_mistral(course_classification(stigma)))
            disrupt[stigma].append(run_mistral(disruptiveness_classification(stigma)))
            aesthetics[stigma].append(run_mistral(aesthetics_classification(stigma)))
            origin[stigma].append(run_mistral(origin_classification(stigma)))
            peril[stigma].append(run_mistral(peril_classification(stigma)))

        #print statement to keep of which stigma the script is on
        print(stigma, 'done')
    
    #return all calls to the model for each stigma and dimension
    return list(visibilities.values()), list(course.values()), list(disrupt.values()), list(aesthetics.values()), list(origin.values()), list(peril.values())

visibilities, course, disrupt, aesthetics, origin, peril = generate_all_data(stigmas_list, 1)

#put into dataframe
data = {'Stigmas': stigmas_list, 'Visibility' : visibilities, 'Course': course, 'Disrupt' : disrupt, 'Aesthetics' : aesthetics,
        'Origin' : origin, 'Peril': peril}

df_mistral = pd.DataFrame(data)

#get the average of each stigma:dimension pair
average_visibility, average_course, average_disrupt, average_aesthetics, average_origin, average_peril = averaged_values(df_mistral)

#attach average values to dataframe (this columns essentially replicate that of Pachankis Table 2)
averaged_data = {'Stigmas': stigmas_list, 'Visibility_average' : average_visibility, 'Course_average': average_course, 'Disrupt_average' : average_disrupt, 'Aesthetics_average' : average_aesthetics,
        'Origin_average' : average_origin, 'Peril_average': average_peril}

#create the final dataframe
final_df = df_mistral.assign(**averaged_data)

#export to a CSV in data files

final_df.to_csv('LLM-output-data/mistral_stigma_perception.csv', index = False)