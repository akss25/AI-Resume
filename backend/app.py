from flask import Flask, request, jsonify, render_template, send_file
from pdfdocument.document import PDFDocument
from flask_cors import CORS
import os
import json
import ast
from openai import OpenAI
import re
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from db import init_db
from token_utils import generate_token  # Import the generate_token function


# from IPython.core.display import display, HTML
app = Flask(__name__)
CORS(app, resources={
    r"/authentication/*": {"origins": "http://localhost:5173"},
    r"/generate_resume": {"origins": "http://localhost:5173"}
})

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# Initialize the MongoDB connection
mongo = init_db(app)


# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Functions for Prompts
def create_prompt(major, industry):
    prompt = f"""Create a resume tailored to {major} and {industry}.
    The resume should be concise, and focus on matching the job description provided.
    Make sure it stands out while accurately reflecting the individual's skills and experiences.
    Honesty is key; only include skills and experiences that the individual actually possesses."""
    return prompt

def generate_initial_user_response(job_role, education, experience_years, skills, job_requirements):

    user_response = f"I'd like to create a resume for a {job_role} position. " \
                    f"I have a {education}, {experience_years} years of experience in full-stack development, " \
                    f"and I'm skilled in languages like {', '.join(skills)}. " \
                    f"I've worked on various projects related to different domains. " \
                    f"The job I'm applying for requires {', '.join(job_requirements)}."
    return user_response

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint for registering user
@app.route('/authentication/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return jsonify({"success": False, "error": "Missing name, email, or password"}), 400
        
        users_collection = mongo.db.users  # Access the 'users' collection

        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "error": "User already exists"}), 409
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password
        }
        
        # Insert the user document
        result = users_collection.insert_one(user_data)
        
        # Retrieve the inserted user document
        new_user = users_collection.find_one({"_id": result.inserted_id})
        
        if new_user:
            token = generate_token(new_user['_id'])
            return jsonify({
                "success": True,
                "message": "User registered successfully",
                "token": token,
                "name": new_user['name'],
                "email": new_user['email']
            }), 201
        else:
            return jsonify({"success": False, "error": "Error retrieving user"}), 500
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


#API endpoint for Login user
@app.route('/authentication/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "error": "Missing email or password"}), 400

        users_collection = mongo.db.users
        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            token = generate_token(user['email'])
            return jsonify({"success": True, "token": token, "name": user['name'], "email": user['email']})
        else:
            return jsonify({"success": False, "error": "Invalid email or password"}), 401

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


# API endpoint for resume generation
@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()

        # Unpack data
        major = data.get('major', '')
        industry = data.get('industry', '')
        job_role = data.get('job_role', '')
        education = data.get('education', '')
        experience_years = data.get('experience_years', '')
        skills = data.get('skills', [])
        job_requirements = data.get('job_requirements', [])

        # PROMPT:1
        max_tokens=50
        q1 = """I'm looking to create a tailored resume for an Application Support role based on a specific job description. 
            The resume should focus on matching the job's requirements and qualifications. Over the next five prompts, I will provide details for the Objective, Skills, Work Experience, Education, and Additional Qualifications sections. 
            Please generate concise and relevant content for each section."""
        system_role_content =create_prompt(major,industry)
        messages = [
            {'role': 'system', 'content': system_role_content},
            {'role': 'user', 'content': q1}
        ]

        response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages= messages,
                temperature=0.3,
                max_tokens=max_tokens
            )
        
        bot_response_1 = response.choices[0].message.content

        # PROMPT:2
        q2="""Here is my objective please rewrite it for clarity: 
            am seeking an Application Support role where I can apply my extensive experience in application tuning, 
            .Net desktop applications, and enterprise-scale systems, preferably in a healthcare setting."""
        messages = [
            {'role': 'system', 'content': system_role_content},
            {'role': 'user', 'content': q1},
            {'role': 'assistant', 'content': bot_response_1},
            {'role': 'user', 'content': q2}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.3,
            max_tokens=max_tokens
        )
        bot_response_2 = response.choices[0].message.content

        # PROMPT:3
        q3=""""Now, let's move on to the Skills section. What technical skills should I include"""
        messages = [
            {'role': 'system', 'content': system_role_content},
            {'role': 'user', 'content': q1},
            {'role': 'assistant', 'content': bot_response_1},
            {'role': 'user', 'content': q2},
            {'role': 'assistant', 'content': bot_response_2},
            {'role': 'user', 'content': q3}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.3,
            max_tokens=max_tokens
        )
        bot_response_3 = response.choices[0].message.content
        
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.3,
            max_tokens=max_tokens
        )
        bot_response_4 = response.choices[0].message.content
        
        
        q5="""Here are my additional qualifications:
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.3,
            max_tokens=max_tokens
        )
        bot_response_5 = response.choices[0].message.content
        

        q6="""""Now that we have all the sections, can you compile them into a complete, well-formatted resume and save the response as python dictionary only, avoid response introduction sentence so that I can easily convert it to one?."""
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.3,
            max_tokens=max_tokens*10
        )
        bot_response_6 = response.choices[0].message.content
        
        q7="""""Great now can you convert this resume to french and save the response as python dictionary only, avoid response introduction sentence so that I can easily convert it to one?."""
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.3,
            max_tokens=max_tokens*10*3
        )
        bot_response_7 = response.choices[0].message.content
        
        def getDictionary(api_response):
            try:
                return ast.literal_eval(api_response)
            except Exception as e:
                print("Error converting string to dictionary:", str(e))

        french_resume = getDictionary(bot_response_7)
        english_resume = getDictionary(bot_response_6)
        # print(french_resume)
        # print(english_resume)
        final_response = {"success": True, "resume": english_resume, "resume_french": french_resume}
        print(final_response)
        return final_response

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
