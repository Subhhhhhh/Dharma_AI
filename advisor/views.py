from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from advisor.models import ChatMessage


def home(request):
    return render(request, 'advisor/home.html')


@login_required
def chat_view(request):
    from advisor.ai_service import generate_dharma_response  # 🔥 LAZY IMPORT

    messages_qs = ChatMessage.objects.filter(user=request.user)

    if request.method == 'POST':
        user_text = request.POST.get('message', '').strip()

        if user_text:
            ChatMessage.objects.create(
                user=request.user,
                role='user',
                text=user_text
            )

            history = [
                {"role": msg.role, "text": msg.text}
                for msg in ChatMessage.objects.filter(
                    user=request.user
                ).order_by('created_at')
            ]

            ai_text = generate_dharma_response(user_text, history=history)

            ChatMessage.objects.create(
                user=request.user,
                role="ai",
                text=ai_text or "🙏 AI is resting now. Please try again later."
            )

            return redirect('advisor:chat')

    return render(request, 'advisor/chat.html', {'chat_messages': messages_qs})


@login_required
def ramayan_ai_view(request):
    from advisor.ramayan_ai_service import generate_ramayan_lesson  # 🔥 LAZY IMPORT

    output = None
    if request.method == "POST":
        message = request.POST.get("message")
        output = generate_ramayan_lesson(message)

    return render(request, "advisor/ramayan_ai.html", {"output": output})


@login_required
def sunderkand_ai_view(request):
    from advisor.sunderkand_ai_service import generate_sunder_story  # 🔥 LAZY IMPORT

    output = None
    if request.method == "POST":
        message = request.POST.get("message")
        output = generate_sunder_story(message)

    return render(request, "advisor/sunderkand_ai.html", {"output": output})


def about_view(request):
    return render(request, 'about.html')


def testimonials_view(request):
    return render(request, 'testimonials.html')


def hanuman_chalisa_view(request):
    return render(request, 'advisor/hanuman_chalisa.html')


def bajrang_baan_view(request):
    return render(request, 'advisor/bajrang_baan.html')


def sankat_mochan_view(request):
    return render(request, 'advisor/sankat_mochan.html')


def Ram_stuti_view(request):
    return render(request, 'advisor/Ram_stuti.html')
