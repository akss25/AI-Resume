#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openai
import os


# In[1]:


#os.environ['OPENAI_API_KEY'] = 'sktest'
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key 


# ## Functions for Prompts

# In[3]:


def create_prompt(major ,industry):
    prompt =  f"""Create a resume tailored to {major} and {industry}. 
The resume should be concise, and focus on matching the job description provided. 
Make sure it stands out while accurately reflecting the individual's skills and experiences. 
Honesty is key; only include skills and experiences that the individual actually possesses."""
    return prompt

# Usage
major = "Computer Science"
result = create_prompt(major,'data')
print(result)


# In[2]:


def generate_initial_user_response(job_role, education, experience_years, skills, job_requirements):
    user_response = f"I'd like to create a resume for a {job_role} position. " \
                    f"I have a {education}, {experience_years} years of experience in full-stack development, " \
                    f"and I'm skilled in languages like {', '.join(skills)}. " \
                    f"I've worked on various projects related to different domains. " \
                    f"The job I'm applying for requires {', '.join(job_requirements)}."
    return user_response

# Example usage:
job_role = "software engineering"
education = "Bachelor's degree in Computer Science"
experience_years = 3
skills = ["Python", "Java", "JavaScript"]
job_requirements = ["strong problem-solving skills", "experience in agile methodologies", "proficiency in Python and cloud services"]

initial_response = generate_initial_user_response(job_role, education, experience_years, skills, job_requirements)
print(initial_response)


# ## First Prompt

# In[3]:


major ='computer science'
industry = 'data science'
system_role_content =create_prompt(major,industry)
max_tokens=50
q1 = """
I'm looking to create a tailored resume for an Application Support role based on a specific job description. 
The resume should focus on matching the job's requirements and qualifications. Over the next five prompts, I will provide details for the Objective, Skills, Work Experience, Education, and Additional Qualifications sections. 
Please generate concise and relevant content for each section."""

messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1}
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens
)


# ## Response

# In[6]:


bot_response_1 = response['choices'][0].message.content


# ## Second Prompt

# In[ ]:


q2="""Here is my objective please rewrite it for clarity: 
am seeking an Application Support role where I can apply my extensive experience in application tuning, 
.Net desktop applications, and enterprise-scale systems, preferably in a healthcare setting."""
messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1},
    {'role': 'assistant', 'content': bot_response_1},
    {'role': 'user', 'content': q2}
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens
)
bot_response_2 = response['choices'][0].message.content


# In[ ]:


print(response['choices'][0].message.content)


# In[10]:


q3=""""Now, let's move on to the Skills section. What technical skills should I include"""
messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1},
    {'role': 'assistant', 'content': bot_response_1},
    {'role': 'user', 'content': q2},
    {'role': 'assistant', 'content': bot_response_2},
    {'role': 'user', 'content': q3}
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens
)
bot_response_3 = response['choices'][0].message.content


# In[11]:


print(bot_response_1)
print(bot_response_2)
print(bot_response_3)


# In[12]:


q4=""""Here is my work experience please reword it based on above discussion:
I have 5 years of experience in application support, focusing on tuning and optimizing large-scale applications. 
I've also been responsible for planning and implementing new technologies in complex, integrated environments.
"""
messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1},
    {'role': 'assistant', 'content': bot_response_1},
    {'role': 'user', 'content': q2},
    {'role': 'assistant', 'content': bot_response_2},
    {'role': 'user', 'content': q3},
    {'role': 'assistant', 'content': bot_response_3},
    {'role': 'user', 'content': q4}
    
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens
)
bot_response_4 = response['choices'][0].message.content


# In[4]:


q5=""""Here are my additional qualifications:
have provided technical support for integrated enterprise-scale systems in a healthcare setting. 
I also have a solid understanding of DevOps principles and tools, 
including GitHub, Artifactory, and Jenkins.
"""
messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1},
    {'role': 'assistant', 'content': bot_response_1},
    {'role': 'user', 'content': q2},
    {'role': 'assistant', 'content': bot_response_2},
    {'role': 'user', 'content': q3},
    {'role': 'assistant', 'content': bot_response_3},
    {'role': 'user', 'content': q4},
    {'role': 'assistant', 'content': bot_response_4},
    {'role': 'user', 'content': q5},
    
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens
)
bot_response_5 = response['choices'][0].message.content


# ## Create the Resume

# In[5]:


q6="""""Now that we have all the sections, can you compile them into a complete, well-formatted resume.
"""
messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1},
    {'role': 'assistant', 'content': bot_response_1},
    {'role': 'user', 'content': q2},
    {'role': 'assistant', 'content': bot_response_2},
    {'role': 'user', 'content': q3},
    {'role': 'assistant', 'content': bot_response_3},
    {'role': 'user', 'content': q4},
    {'role': 'assistant', 'content': bot_response_4},
    {'role': 'user', 'content': q5},
    {'role': 'assistant', 'content': bot_response_5},
    {'role': 'user', 'content': q6}
    
    
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens*10
)
bot_response_6 = response['choices'][0].message.content


# ## Put the resume in french

# In[15]:


q7="""""Great now can you convert this resume to french and save the response as python dictionary so that I can easily convert it to one?.
"""
messages = [
    {'role': 'system', 'content': system_role_content},
    {'role': 'user', 'content': q1},
    {'role': 'assistant', 'content': bot_response_1},
    {'role': 'user', 'content': q2},
    {'role': 'assistant', 'content': bot_response_2},
    {'role': 'user', 'content': q3},
    {'role': 'assistant', 'content': bot_response_3},
    {'role': 'user', 'content': q4},
    {'role': 'assistant', 'content': bot_response_4},
    {'role': 'user', 'content': q5},
    {'role': 'assistant', 'content': bot_response_5},
    {'role': 'user', 'content': q6},
    {'role': 'assistant', 'content': bot_response_6},
    {'role': 'user', 'content': q7}
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0.3,
    max_tokens=max_tokens*10*3
)
bot_response_7 = response['choices'][0].message.content


# In[16]:


from pprint import pprint
pprint(bot_response_7)


# In[17]:


from IPython.core.display import display, HTML
display(HTML(bot_response_6))
