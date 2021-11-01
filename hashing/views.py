from django.shortcuts import render
from .forms import HashForm
from .models import Hash
from django.shortcuts import redirect
from django.http import JsonResponse
import hashlib


def home(request):
    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data['text']
            text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            try:
                Hash.objects.get(hash=text_hash)
            except Hash.DoesNotExist:
                hash_ = Hash()
                hash_.text = text
                hash_.hash = text_hash
                hash_.save()
            return redirect('hash', hash=text_hash)

    form = HashForm()
    return render(request, 'hashing/home.html', {
        'form': form
    })


def hash(request, hash):
    hash_model = Hash.objects.get(hash=hash)
    return render(request, 'hashing/hash.html', {
        'hash': hash_model
    })


def quick_hash(request):
   text = request.GET['text']
   return JsonResponse({
       'hash': hashlib.sha256(text.encode('utf-8')).hexdigest()
   })
