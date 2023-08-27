from typing import Any, Dict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
import json

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from .models import NewData, PipeData, Unit
from .forms import UploadDataForm, PipeDataForm
from .simulation import leakSimulation, chartSimulation

# Create your views here.
class HomePageview(TemplateView):
    pass

def HomePageView(request):
    if request.method == "POST":
        new_request = request.POST
        # Creates a NewData object using information existing in request.POST
        if "label" in new_request:
            newDataObj = NewData(
                label = new_request["label"],
                density = new_request["density"],
                data = request.FILES["data"],
            )
            newDataObj.save()
            return redirect(reverse("homepage"))
        else:
            request_unit = Unit.objects.get(pk=new_request["unit"])
            request_fluid_data = NewData.objects.get(pk=new_request["fluid_data"])
            newPipeDataObj = PipeData(
                unit = request_unit,
                diameter = new_request["diameter"],
                length = new_request["length"],
                fluid_data = request_fluid_data,
            )
            newPipeDataObj.save()
            return redirect(reverse("homepage"))

    else:
        upload_data = UploadData.as_view()(request)
        pipe_data = PipeDataView.as_view()(request)
        context = {
            "greeting": "Hello world!",
            "availableData": NewData.objects.all(),
            "availablePipeData": PipeData.objects.all(),
        }

        context.update(upload_data.context_data)
        context.update(pipe_data.context_data)

        return render(request, "index.html", context)

class UploadData(CreateView):
    model = NewData
    form_class = UploadDataForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dataForm"] = context["form"]
        return context

class PipeDataView(CreateView):
    model = PipeData
    form_class = PipeDataForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pipeDataForm"] = context["form"]
        return context

def simulationView(request):
    if request.method == "POST":
        try:
            # Gets the json data from the request
            data = json.loads(request.body)
            pipe_label = data.get("pipe_label")

            pipe_datas = PipeData.objects.all()

            # Finds pipe data which corresponds to obtained json data
            for pipe_data in pipe_datas:
                if pipe_data.fluid_data.label == pipe_label:
                    fluid_data = f"uploads/{pipe_data.fluid_data.data}"
                    density = pipe_data.fluid_data.density
                    diameter = pipe_data.diameter
                    length = pipe_data.length

                    result = {}

                    detected_leaks = leakSimulation(fluid_data, density, diameter)
                    for detected_leak in detected_leaks:
                        id = detected_leaks.index(detected_leak) + 1
                        chartTitle = f"{pipe_label}_{detected_leak.location}_{detected_leak.size}"
                        v_plot, p_plot = chartSimulation(fluid_data, chartTitle)

                        leak_status = {
                            f"leak{id}": {
                                "leak_location": detected_leak.location,
                                "leak_size": detected_leak.size,
                                "v_plot": v_plot,
                                "p_plot": p_plot,
                            }
                        }

                        result.update(leak_status)
                    
                    return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        
