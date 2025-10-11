from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CreateTicketForm, FilterTicketForm
from .models import Ticket, Asignacion
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages


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
    desarrolladores = User.objects.filter(is_staff=True)
    html = render_to_string(
        'user/partials/ticket_detalle.html',
        {
            'ticket': ticket,
            'desarrolladores': desarrolladores
        },
        request=request
    )

    return JsonResponse({'html': html})

@login_required
@require_POST
def del_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    
    return redirect('useradm_dashboard')

@login_required
@require_POST
def asignar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    dev_id = request.POST.get('desarrollador')
    prioridad = request.POST.get('prioridad')

    if not dev_id or not prioridad:
        messages.error(request, "Por favor selecciona un desarrollador y una prioridad.")
        return redirect('useradm_dashboard')

    try:
        desarrollador = User.objects.get(id=dev_id)
    except User.DoesNotExist:
        messages.error(request, "El desarrollador seleccionado no existe.")
        return redirect('useradm_dashboard')

    asignacion, created = Asignacion.objects.update_or_create(
        ticket=ticket,
        defaults={'desarrollador': desarrollador, 'prioridad': prioridad}
    )

    ticket.estado_id = 2
    ticket.save()

    if created:
        messages.success(
            request,
            f"✅ Ticket #{ticket.id} asignado a {desarrollador.username} con prioridad {prioridad}. Estado actualizado a 'En Proceso'."
        )
    else:
        messages.info(
            request,
            f"🔄 Ticket #{ticket.id} reasignado a {desarrollador.username}. Estado actualizado a 'En Proceso'."
        )

    return redirect('useradm_dashboard')

@login_required
@require_POST
def cerrar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    ticket.estado_id = 4
    ticket.save()

    return redirect('useradm_dashboard')