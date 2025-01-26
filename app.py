from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
import streamlit as st
from flask import Flask ,render_template,request
import os

os.getenv('LANGCHAIN_API_KEY')
os.getenv('GOOGLE_API_KEY')

prompt = ChatPromptTemplate.from_messages([
    ('system','''You are a doctor with a great knowledge of the diseases and the symptoms of those diseases and you are also well known about the doctors who deal with those diseases now you will be given the input of symptoms a patient is facing and you should tell him  about which disease he is having and suggest which specialist doctor he should consult  and also give him the very basic preventive measures before meeting the doctor but you should not provide any medication, when you will provide the possible causes provide the respective specialist doctor for each cause''' ),
    ('user','''These are the symptoms i am having
     symptoms of patient: {symptoms}
     here is the refernece about how you should generate the content
     {{  
         Possible Causes:
         respective doctor for each cause
         When to Seek Medical Attention:
         Recommended Actions:  }}
     ''')
])

llm= GoogleGenerativeAI(model='gemini-pro')
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

'''st.title('Heal.io')
input_text=st.text_input('enter your symptoms:')

if input_text:
    st.write(chain.invoke({'symptoms':input_text}))'''
    


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page')
def page():
    return render_template('page.html')

@app.route('/predict', methods=['POST'])
def predict():
    data1=request.form['entered']
    response = chain.invoke({'symptoms':data1})
    formatted_response = format_response(response)
    return render_template('page.html', response=formatted_response)
    
def format_response(response):
    lines = response.split('\n')
    formatted_lines = []
    for line in lines:
        if line.startswith('**Possible Causes:**'):
            formatted_lines.append('<strong>Possible Causes:</strong>')
        elif line.startswith('**Respective Doctor for Each Cause:**'):
            formatted_lines.append('<strong>Respective Doctor for Each Cause:</strong>')
        elif line.startswith('**Respective Specialist Doctors:**'):
            formatted_lines.append('<strong>Respective Specialist Doctors:</strong>')    
        elif line.startswith('**When to Seek Medical Attention:**'):
            formatted_lines.append('<strong>When to Seek Medical Attention:</strong>')
        elif line.startswith('**Recommended Actions:**'):
            formatted_lines.append('<strong>Recommended Actions Before Meeting the Doctor:</strong>')
        elif line.startswith('**Recommended Actions:**'):
            formatted_lines.append('<strong>Recommended Actions Before Meeting the Doctor:</strong>')    
        elif line.startswith('**preventive measures:**'):
            formatted_lines.append('<strong>Preventive Measures:</strong>')    
        else:
            formatted_lines.append(line.replace('*', ''))  
    return '<br>'.join(formatted_lines)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)    

   