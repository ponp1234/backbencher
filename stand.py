from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Configure the Gemini API
genai.configure(api_key='AIzaSyB265GIXXq5REPMHi_y_X1luKzaDFtgR6E')

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

@app.route('/ask-ai', methods=['POST'])
def ask_gemini():
    try:
        data = request.json
        question = data['messages'][0]['content']
        
        # Add better error handling and logging
        print(f"Received question: {question}")  # Debug log
        
        # Structure the prompt
        prompt = f"""Please help explain this exam question and provide guidance while maintaining academic integrity. 
        Question: {question}
        Please provide:
        1. A clear explanation of the question
        2. Key concepts to consider
        3. Approach to solving it (without giving the answer)
        """
        
        try:
            # Generate response using Gemini
            response = model.generate_content(prompt)
            
            # Debug logging
            print("API Response received")
            
            return jsonify({
                'response': response.text if hasattr(response, 'text') else str(response)
            })
            
        except Exception as api_error:
            print(f"Gemini API error: {str(api_error)}")  # Debug log
            return jsonify({
                'error': f"Gemini API error: {str(api_error)}"
            }), 500
    
    except Exception as e:
        print(f"Server error: {str(e)}")  # Debug log
        return jsonify({
            'error': f"Server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)