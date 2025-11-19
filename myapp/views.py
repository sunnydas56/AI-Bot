from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

from .forms import StudentSignupForm
from .models import Student, ChatSession, ChatMessage
from .utils import CareerChatbot

def landing(request):
    """Main landing page"""
    return render(request, 'landing.html')

def signup(request):
    """Student signup view"""
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            student = form.save()
            request.session['student_id'] = student.id
            request.session['student_name'] = student.name
            request.session['student_interests'] = student.interests
            return redirect('chat_interface')
    else:
        form = StudentSignupForm()
    
    return render(request, 'signup.html', {'form': form})

def chat_interface(request):
    """Main chat interface"""
    student_id = request.session.get('student_id')
    student_name = request.session.get('student_name', 'Student')
    
    if not student_id:
        return redirect('signup')
    
    # Predefined prompts
    prompts = [
        {"text": "Best career options after Class 10", "icon": "fa-graduation-cap"},
        {"text": "How to choose the right stream", "icon": "fa-stream"},
        {"text": "Career options in Science stream", "icon": "fa-flask"},
        {"text": "Career options in Commerce stream", "icon": "fa-chart-line"},
        {"text": "Career options in Arts stream", "icon": "fa-palette"},
        {"text": "Skills I should develop", "icon": "fa-tools"},
    ]
    
    context = {
        'student_name': student_name,
        'prompts': prompts,
    }
    
    return render(request, 'chat.html', context)

@csrf_exempt
def chat_api(request):
    """API endpoint for chatbot interactions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            session_id = data.get('session_id', '')
            
            # Get or create chat session
            if not session_id:
                session_id = str(uuid.uuid4())
                student_id = request.session.get('student_id')
                if student_id:
                    student = Student.objects.get(id=student_id)
                    ChatSession.objects.create(
                        student=student,
                        session_id=session_id
                    )
            
            # Get student data for personalized responses
            student_data = None
            student_id = request.session.get('student_id')
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                    student_data = {
                        'name': student.name,
                        'class': student.student_class,
                        'interests': student.interests,
                        'goals': student.goals
                    }
                except Student.DoesNotExist:
                    pass
            
            # Generate AI response
            chatbot = CareerChatbot()
            response = chatbot.generate_response(message, student_data)
            
            # Save messages to database if student is logged in
            if student_id:
                try:
                    session = ChatSession.objects.get(session_id=session_id)
                    ChatMessage.objects.create(
                        session=session,
                        message=message,
                        is_user=True
                    )
                    ChatMessage.objects.create(
                        session=session,
                        message=response,
                        is_user=False
                    )
                except ChatSession.DoesNotExist:
                    pass
            
            return JsonResponse({
                'response': response,
                'session_id': session_id
            })
            
        except Exception as e:
            return JsonResponse({
                'error': 'An error occurred while processing your message.',
                'session_id': session_id
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)