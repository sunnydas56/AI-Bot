import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CareerChatbot:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY') or "demo-key"
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        # Career-related keywords for guardrails
        self.career_keywords = [
            'career', 'stream', 'science', 'commerce', 'arts', 'humanities', 'job', 'profession',
            'occupation', 'vocation', 'engineering', 'medical', 'doctor', 'engineer', 'accountant',
            'business', 'finance', 'economics', 'biology', 'physics', 'chemistry', 'mathematics',
            'literature', 'history', 'geography', 'psychology', 'sociology', 'law', 'architecture',
            'design', 'technology', 'computer', 'software', 'hardware', 'data', 'analytics',
            'management', 'marketing', 'sales', 'entrepreneur', 'startup', 'research', 'development',
            'education', 'teaching', 'professor', 'teacher', 'coach', 'trainer', 'consultant',
            'writer', 'author', 'journalist', 'editor', 'artist', 'musician', 'actor', 'director',
            'producer', 'photographer', 'chef', 'hotel', 'tourism', 'hospitality', 'fashion',
            'model', 'designer', 'sports', 'athlete', 'player', 'coach', 'fitness', 'health',
            'nutrition', 'dietitian', 'physician', 'surgeon', 'dentist', 'veterinary', 'nurse',
            'pharmacist', 'therapist', 'psychologist', 'counselor', 'social', 'worker', 'police',
            'army', 'navy', 'airforce', 'pilot', 'astronaut', 'scientist', 'researcher', 'analyst',
            'programmer', 'developer', 'web', 'app', 'mobile', 'game', 'graphic', 'animation',
            'digital', 'media', 'content', 'creator', 'influencer', 'youtuber', 'blogger', 'vlogger',
            'streamer', 'gamer', 'esports', 'cyber', 'security', 'hacker', 'ethical', 'cloud',
            'ai', 'artificial', 'intelligence', 'machine', 'learning', 'blockchain', 'crypto',
            'bitcoin', 'ethereum', 'nft', 'metaverse', 'virtual', 'reality', 'augmented', 'ar', 'vr'
        ]
    
    def is_career_related(self, message):
        """Check if the message is career-related"""
        lower_message = message.lower()
        return any(keyword in lower_message for keyword in self.career_keywords)
    
    def generate_response(self, message, student_data=None):
        """Generate AI response for career-related queries"""
        
        # Check if message is career-related
        if not self.is_career_related(message):
            return "I'm designed to help with career-related questions only. Please ask me about career options, stream selection, skills development, or similar topics."
        
        # For demo purposes - in production, use actual OpenAI API
        if self.api_key == "demo-key":
            return self._get_demo_response(message, student_data)
        
        # Actual OpenAI API integration
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = self._build_prompt(message, student_data)
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a career guidance counselor for Class 10 students. Provide helpful, accurate information about career options, stream selection, and educational pathways. Keep responses concise and engaging.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 500,
                'temperature': 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            return self._get_demo_response(message, student_data)
    
    def _build_prompt(self, message, student_data):
        """Build the prompt for the AI"""
        base_prompt = f"Student question: {message}\n\n"
        
        if student_data:
            base_prompt += f"Student details:\n"
            base_prompt += f"Name: {student_data.get('name', 'Not provided')}\n"
            base_prompt += f"Class: {student_data.get('class', 'Not provided')}\n"
            base_prompt += f"Interests: {student_data.get('interests', 'Not provided')}\n"
            base_prompt += f"Goals: {student_data.get('goals', 'Not provided')}\n\n"
        
        base_prompt += "Please provide a helpful, concise response about career guidance for a Class 10 student."
        return base_prompt
    
    def _get_demo_response(self, message, student_data):
        """Generate demo responses when API is not available"""
        lower_message = message.lower()
        
        if 'career option' in lower_message or 'what can i do' in lower_message:
            interests = student_data.get('interests', 'various fields') if student_data else 'various fields'
            return f"""After Class 10, you have several career paths to consider. The main streams are:

1. Science - Leads to careers in Engineering, Medicine, Research, Technology, etc.
2. Commerce - Opens doors to Business, Finance, Accounting, Economics, etc.
3. Arts/Humanities - Offers careers in Literature, History, Psychology, Design, Law, etc.

Based on your interests in {interests}, I can provide more specific guidance. What stream are you most curious about?"""

        elif 'stream' in lower_message or 'choose' in lower_message:
            interests = student_data.get('interests', 'various fields') if student_data else 'various fields'
            return f"""Choosing the right stream after Class 10 is an important decision. Here's a brief overview:

• Science Stream: Focuses on Physics, Chemistry, Biology, and Mathematics. Ideal if you're interested in medicine, engineering, research, or technology.

• Commerce Stream: Includes Accountancy, Business Studies, Economics. Great for careers in finance, business management, entrepreneurship, or economics.

• Arts/Humanities: Covers subjects like History, Geography, Political Science, Psychology. Perfect for careers in law, civil services, teaching, writing, or social sciences.

Your interests in {interests} might align well with certain streams. Would you like more details about any specific stream?"""

        elif 'science' in lower_message:
            return """The Science stream offers diverse career options:

• Medical Field: Doctor, Surgeon, Dentist, Veterinarian, Pharmacist, Physiotherapist
• Engineering: Mechanical, Civil, Computer Science, Electrical, Aerospace, Chemical
• Research: Scientist in various fields, Research Analyst, Lab Technician
• Technology: Software Developer, Data Scientist, AI Engineer, Cybersecurity Expert
• Other Fields: Architecture, Biotechnology, Environmental Science, Forensic Science

Science requires strong analytical skills and interest in mathematics and scientific concepts. Would you like to know about specific science careers?"""

        elif 'commerce' in lower_message:
            return """Commerce stream leads to various business and finance careers:

• Accounting: Chartered Accountant, Cost Accountant, Company Secretary
• Finance: Investment Banker, Financial Analyst, Wealth Manager, Bank PO
• Business: Business Management, Entrepreneurship, Marketing, HR
• Economics: Economist, Policy Analyst, Statistician, Data Analyst
• Other Fields: Actuary, Stockbroker, Insurance Advisor, Tax Consultant

Commerce is ideal if you have an interest in numbers, business trends, and economic principles. Would you like details about any specific commerce career?"""

        elif 'arts' in lower_message or 'humanities' in lower_message:
            return """Arts/Humanities stream offers creative and social science careers:

• Literature & Languages: Writer, Editor, Journalist, Translator, Professor
• Social Sciences: Psychologist, Sociologist, Historian, Archaeologist, Anthropologist
• Law & Governance: Lawyer, Judge, Civil Servant, Politician, Diplomat
• Creative Arts: Artist, Musician, Actor, Director, Designer, Architect
• Education: Teacher, Professor, Educational Consultant, Counselor
• Other Fields: Tourism, Hospitality, Fashion, Media, Public Relations

Humanities develop critical thinking, communication, and analytical skills. Would you like information about specific arts careers?"""

        elif 'skill' in lower_message:
            interests = student_data.get('interests', 'various fields') if student_data else 'various fields'
            return f"""Developing the right skills is crucial for career success. Here are important skills to focus on:

• Communication Skills: Writing, public speaking, presentation skills
• Digital Literacy: Basic computer skills, coding, data analysis
• Critical Thinking: Problem-solving, analytical reasoning, decision-making
• Creativity: Innovation, design thinking, artistic expression
• Collaboration: Teamwork, leadership, interpersonal skills
• Adaptability: Learning agility, flexibility, resilience

Based on your interest in {interests}, I recommend focusing on developing a combination of technical and soft skills relevant to your chosen field. Would you like more specific skill development advice?"""

        else:
            interests = student_data.get('interests', 'various fields') if student_data else 'various fields'
            return f"""I understand you're asking about career guidance. Based on your interests in {interests}, I recommend exploring careers that align with your passions and strengths.

Would you like me to provide more specific information about:
• Career options in a particular field
• How to prepare for a specific career
• Skills needed for different professions
• Educational pathways after Class 10

Feel free to ask me any specific career-related questions!"""