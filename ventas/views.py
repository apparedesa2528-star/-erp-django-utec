
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from xhtml2pdf import pisa

from configuracion.models import ConfiguracionERP
from .forms import DetalleVentaForm, VentaForm
from .models import DetalleVenta, Venta


# ── VISTAS DE VENTAS ────────────────────────────────────────────────────

class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/lista.html'
    context_object_name = 'ventas'
    paginate_by = 10
    ordering = ['-fecha']


class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/detalle.html'
    context_object_name = 'venta'
    pk_url_kwarg = 'venta_id'


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Venta
    template_name = 'ventas/eliminar.html'
    pk_url_kwarg = 'venta_id'
    success_url = reverse_lazy('ventas:lista')


@login_required
def crear_venta(request):
    """Crea un encabezado de venta con una línea de detalle."""

    venta_form = VentaForm(request.POST or None)
    detalle_form = DetalleVentaForm(request.POST or None)

    if request.method == 'POST':
        if venta_form.is_valid() and detalle_form.is_valid():
            venta = venta_form.save()

            detalle = detalle_form.save(commit=False)
            detalle.venta = venta
            detalle.save()

            messages.success(
                request,
                f'Venta #{venta.pk} registrada. '
                f'Total: ${venta.total:.2f}',
            )

            return redirect(
                'ventas:detalle',
                venta_id=venta.pk,
            )

    return render(
        request,
        'ventas/crear.html',
        {
            'venta_form': venta_form,
            'detalle_form': detalle_form,
        },
    )


# ── VISTA W12: FACTURA PDF ──────────────────────────────────────────────

@login_required
def venta_pdf(request, venta_id: int) -> HttpResponse:
    """Genera y descarga la factura PDF de una venta."""

    venta = get_object_or_404(
        Venta.objects.select_related(
            'cliente',
        ).prefetch_related(
            'detalles__producto',
        ),
        pk=venta_id,
    )

    config = ConfiguracionERP.get_instance()

    context = {
        'venta': venta,
        'config': config,
    }

    html_string = render_to_string(
        'ventas/factura_pdf.html',
        context,
    )

    buffer = io.BytesIO()

    pisa_status = pisa.CreatePDF(
        html_string,
        dest=buffer,
    )

    if pisa_status.err:
        return HttpResponse(
            'Error al generar el PDF',
            status=500,
        )

    buffer.seek(0)

    response = HttpResponse(
        buffer.read(),
        content_type='application/pdf',
    )

    response['Content-Disposition'] = (
        f'attachment; filename="factura_{venta.pk:05d}.pdf"'
    )

    return response
