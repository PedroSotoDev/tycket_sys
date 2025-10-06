from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateTicketForm, FilterTicketForm, EditTicketForm
from .models import Ticket, Asignacion
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required(login_url="/login")
def user_dashboard(req):
    tickets = Ticket.objects.filter(creador=req.user)

    if req.method == "POST":
        form = CreateTicketForm(req.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creador = req.user
            ticket.save()
            return redirect('user_dashboard')
    else:
        form = CreateTicketForm()

    return render(req, "user/user_dashboard.html", {
        "tickets": tickets,
        "form": form
    })

@login_required
def useradm_dashboard(request):
    tickets = Ticket.objects.select_related('categoria', 'estado', 'asignacion').all()
    form = FilterTicketForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data.get('estado'):
            tickets = tickets.filter(estado=form.cleaned_data['estado'])
        if form.cleaned_data.get('categoria'):
            tickets = tickets.filter(categoria=form.cleaned_data['categoria'])
        if form.cleaned_data.get('desarrollador'):
            tickets = tickets.filter(asignacion__desarrollador=form.cleaned_data['desarrollador'])

    return render(request, "user/useradm_dashboard.html", {
        "tickets": tickets,
        "form": form
    })


@login_required
def ticket_detalle(request, ticket_id):
    ticket = get_object_or_404(
        Ticket.objects.select_related('categoria', 'estado', 'asignacion__desarrollador'),
        id=ticket_id
    )
    html = render_to_string('user/partials/ticket_detalle.html', {'ticket': ticket}, request=request)

    return JsonResponse({'html': html})

