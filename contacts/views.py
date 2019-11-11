from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail


def contact(request):
    if request.method=='POST':
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']

        #check if inquiry is already been sent
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted =  Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already made inquiry for this listing")
                return redirect ('/listings/'+listing_id)



        contact=Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        #send email upon inquiry
        send_mail(
            'Testing backend real estate project',
            'You have been provided with inquiry for '+ listing +'. Please check it out in admin area.',
            'dilearnstocode@hotmail.com',
            ['duran.irnes@gmail.com'],
            fail_silently=False,
            )
        messages.success(request, "Your message has been submitted, a realtor will get back to you soon")
        return redirect ('/listings/'+listing_id)
