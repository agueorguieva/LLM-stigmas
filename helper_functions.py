import numpy as np
import re 

stigmas_list = ["Autism or Autism Spectrum Disorder", "Bipolar Disorder Symptomatic", "Blind Completely", "Cleft Lip And Palate Current", "Deaf Completely", 
                "Facial Scars", "Mental Retardation", "Movement/Gait Impairment Current Average Severity", "Schizophrenia Symptomatic",
                "Short", "Speech Disability", "Stroke recent average impairment", "Unattractive", "Using a Wheelchair all the Time", " Alcohol Dependency Current",
                "Bacterial Sexually Transmitted Disease", "Cocaine use recreationally", "Criminal Record", "Crystal Methamphetamine Use Recreationally", 
                "Drug Dealing", "Drug Dependency Current", "Gang Member Currently", "Genital Herpes", "HIV Average Symptoms", "Homeless", "Injection Drug Use", "On Parole Currently",
                "Sex Offender", "Asian American", "Black/African American", "Latina/Latino", "Middle Eastern", "Multiracial",  "Native American",
                "Old Age", "South Asian", "Asexual", "Atheist", "Bipolar Disorder Remitted", "Breast Cancer Current Average Symptoms",
                "Breast Cancer Remitted", "Chest Scars","Colorectal Cancer Current Average Symptoms", "Colorectal Cancer Remitted", "Depression Remitted", "Diabetes Type 2",
                "Divorced Previously", "Documented Immigrant", "Fundamentalist Christian", "Had an Abortion Previously",
                "Heart Attack Recent Average Impairment", "Infertile", "Intersex", "Jewish", "Lesbian/Gay/Bisexual/Nonheterosexual",
                "Less Than a High School Education", "Limb Scars", "Lung Cancer Current Average Symptoms","Lung Cancer Remitted", 
                "Movement/Gait Impairment Remitted Average Severity", "Prostate Cancer Current Average Symptoms","Prostate Cancer Remitted","Psoriasis Remitted Average Severity",
                "Teen Parent Currently", "Teen Parent Previously","Unemployed", "Voluntarily Childless", "Was Raped Previously",
                "Working Class or Poor", "Working in a Manual Industry", "Working in a Service Industry","Alcohol Dependency Remitted",
                "Depression Symptomatic", "Drug Dependency Remitted", "Fat/Overweight/Obese Current Average Severity", 
                "Fat/Overweight/Obese Remitted Average Severity","Fecal Incontinence",
                "Having Sex for Money", "Illiteracy","Living in a Trailer Park", "Living in Public Housing", "Marijuana Use Recreationally",
                "Multiple Body Piercings", "Multiple Facial Piercings", "Multiple Tattoos","Muslim", "Polyamorous", "Psoriasis Current Average Severity",
                "Schizophrenia Remitted", "Smoking Cigarettes Daily", "Transgender", "Undocumented Immigrant", "Urinary Incontinence"]

#prompts that include specifics on 1 through 5 classification
def concealability_classification(inquiry):
    user_message = (
        f"""
        You are a member of the general American public. The user will provide you with a condition or identity and you must answer: 
            How easily is this condition or identity able to be concealed in a typical social interaction between typical members
            of the United States population?

        Answer the question by categorizing the condition or identity after <<<>>> into one of the following predefined categories:
            
        "0 - totally concealable in casual social interaction"
        "1 - almost always concealable in casual social interaction"
        "2 - more concealable in casual social interaction"
        "3 - both concealable and not concealable in casual social interaction"
        "4 - less concealable in casual social interaction"
        "5 - almost never able to be concealed in casual social interaction"
        "6 - never able to be concealed in casual social interaction"

        If the text doesn't fit into any of the above categories, classify it as:
        Unsure

        You will only respond with the predefined category and the output must start with a number. Do not explain.

        <<<
        Inquiry: {inquiry}
        >>>
        """
        )
    return user_message


def course_classification(inquiry):
    user_message = (
        f"""
        You are a member of the general American public. The user will provide you with a condition or identity and you must answer: 
            To what extent does the general U.S. population expect the condition or identity to improve or persist, worsen, or recur? 
        
        Answer the question by categorizing the condition or identity after <<<>>> into one of the following predefined categories:

        "0 - temporary, expected to totally disappear over a short period of time"
        "1 - almost temporary, expected to totaly disappear over a long period of time"
        "2 - slightly temporary, expected to partially disappear over a long period of time"
        "3 - can be changed, but unsure"
        "4 - slightly persistent, expected to remain but to a much lower degree"
        "5 - almost persistent, expected to remain slightly unchanged"
        "6 - persistent, expected to remain unchanged, worsen, or recur over the life course"

        If the text doesn't fit into any of the above categories, classify it as:
        unsure

        You will only respond with the predefined category and the output must start with a number. Do not explain.

        <<<
        Inquiry: {inquiry}
        >>>
        """
    )
    return user_message

def disruptiveness_classification(inquiry):
    user_message = (
        f"""
        You are a member of the general American public. The user will provide you with a condition or identity and you must answer: 
            To what extent does the condition or identity disrupt typical social interactions taking place among typical members of the 
            U.S. population, assuming the stigma is known?
        
        Answer the question by categorizing the condition or identity after <<<>>> into one of the following predefined categories:

        "0 - normal social interaction is not disruptted at all"
        "1 - normal social interaction is rarely disrupted"
        "2 - normal social interaction is sometimes disrupted, but not too much"
        "3 - normal social interaction can be both disrupted and not disrupted"
        "4 - normal social interaction is sometimes disrupted, more often than not"
        "5 - normal social interaction is often disrupted"
        "6 - normal social interaction is extremely difficult"
        
        If the text doesn't fit into any of the above categories, classify it as:
        unsure

        You will only respond with the predefined category and the output must start with a number. Do not explain. 

        <<<
        Inquiry: {inquiry}
        >>>
        """
    )
    return user_message

def aesthetics_classification(inquiry):
    user_message = (
        f"""
        You are a member of the general American public. The user will provide you with a condition or identity and you must answer: 
            To what extent does the condition prompt physical revulsion among typical members of the U.S. population in typical 
            social interactions, assuming the stigma is known?

        Answer the question by categorizing the condition or identity after <<<>>> into one of the following predefined categories:

        "0 - condition or identity is not generally seen as repulsive"
        "1 - condition or identity is rarely seen as repulsive, but it can happen"
        "2 - condition or identity can sometimes be repulsive"
        "3 - condition or identity is can be seen as both repulsive and not repulsive, depending on the situation"
        "4 - condition or identity is generally seen as somewhat repulsive"
        "5 - condition or identity is generally seen as repulsive"
        "6 - condition or identity is generally seen as extremely repulsive"
        
        If the text doesn't fit into any of the above categories, classify it as:
        unsure

        You will only respond with the predefined category and the output must start with a number. Do not explain.

        <<<
        Inquiry: {inquiry}
        >>>
        """
    )
    return user_message

def origin_classification(inquiry):
    user_message = (
        f"""
        You are a member of the general American public. The user will provide you with a condition or identity and you must answer: 
            To what extent do people in the United States generally see the stigmatized individual as being responsible for his or her 
            condition or identity?
        
        Answer the question by categorizing the condition or identity after <<<>>> into one of the following predefined categories:

        "0 - condition is seen as totally out of the individual’s control"
        "1 - condition is seen as mostly out of the individual's control"
        "2 - condition is seen as not in the indvidiual's control, more often than not"
        "3 - condition is both in their control and out of their control"
        "4 - condition is seen as in the indvidiual's control, more often than not"
        "5 - condition is seen as mostly under the individual's control"
        "6 - condition is seen as totally under the individual’s control"
        
        If the text doesn't fit into any of the above categories, classify it as:
        unsure

        You will only respond with the predefined category and the output must start with a number. Do not explain.

        <<<
        Inquiry: {inquiry}
        >>>
        """
    )
    return user_message

def peril_classification(inquiry):
    user_message = (
        f"""
        You are a member of the general American public. The user will provide you with a condition or identity and you must answer: 
            In the general U.S. population, to what extent do people who interact with the stigmatized individual perceive 
            some kind of contagion, threat, peril, or physical danger to themselves in typical social interactions, 
            assuming the stigma is known?

        Answer the question by categorizing the condition or identity after <<<>>> into one of the following predefined categories:

        "0 - there is no perceived contagion, peril, or physical danger to oneself"
        "1 - there is almost no perceived contagion, peril, or physical danger to oneself"
        "2 - there is a small perceived contagion, period, or physical danger to oneself"
        "3 - there is a 50% chance of perceived contagion, peril, or physical danger to oneself"
        "4 - there is a greater perceived contagion, peril, or physical danger to oneself"
        "5 - there is almost always a perceived contagion, peril, or physical danger to oneself"
        "6 - there is extreme perceived contagion, peril, or physical danger to oneself"
        
        If the text doesn't fit into any of the above categories, classify it as:
        unsure

        You will only respond with the predefined category and the output must start with a number. Do not explain. 

        <<<
        Inquiry: {inquiry}
        >>>
        """
    )
    return user_message

def extract_value(input_string, model):

    if model == 'mistral':
        #Checking to see if the output is a number(integer or decimal) after [/INST]
        number = re.search(r'\[/INST\].*?(\d+(\.\d+)?)', input_string)

        #Checking to see if output is a word
        word = re.search(r'\[/INST\]\s*([a-zA-Z]+)', input_string)

        if number:
            return float(number.group(1)) #return first number as a float
        elif word:
            if (word.group(1)).lower() == "unsure": #return unsure if the model gave 'unsure'
                return "unsure"
        else:
            return 'Improper output'
    
    elif model == 'granite':
         #Checking to see if the output is a number(integer or decimal) after end of role
        number = re.search(r'<\|end_of_role\|>(\d+)', input_string)

        #Checking to see if output is a word
        word = re.search(r'<\|end_of_role\|>\s*(\w+)', input_string)

        if number:
            return float(number.group(1))  #return the number as a float
        elif word:
            if (word.group(1)).lower() == "unsure": #return unsure if the model gave 'unsure'
                    return "unsure"
        else:
            return "Improper outout" 
        

def take_average(values):
    #remove any values that are not floats
    floats_only = [x for x in values if isinstance(x, float)]

    if floats_only == []:
        return 'No numerical outputs given'
    return round(np.mean(floats_only), 2)

def averaged_values(df):
    average_visibility = []
    average_course = []
    average_disrupt = []
    average_aesthetics = []
    average_origin = []
    average_peril = []

    for one_row in df['Visibility']:
        average_visibility.append(take_average(one_row))

    for one_row in df['Course']:
        average_course.append(take_average(one_row))

    for one_row in df['Disrupt']:
        average_disrupt.append(take_average(one_row))

    for one_row in df['Aesthetics']:
        average_aesthetics.append(take_average(one_row))

    for one_row in df['Origin']:
        average_origin.append(take_average(one_row))

    for one_row in df['Peril']:
        average_peril.append(take_average(one_row))

    return average_visibility, average_course, average_disrupt, average_aesthetics, average_origin, average_peril