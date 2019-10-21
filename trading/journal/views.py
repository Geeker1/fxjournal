# Django Imports
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import Context, engines
from django.template.backends.utils import csrf_token_lazy
from django.utils.dateparse import parse_date

# Dependency Imports
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Application Imports
from .forms import ForexEntryForm, BinaryEntryForm, StampForm,\
    ReasonForm, LessonForm
from .models import ForexEntry, BinaryEntry, TimeStamp
from .serializers import StampSerializer, BinarySerializer, ForexSerializer


LINK_FOREX = "journal/fx.html"
LINK_BINARY = "journal/binary.html"
LINK_STAMP = "journal/stamp.html"

engine = engines['django'].engine
fx_template = engine.get_template(LINK_FOREX)
binary_template = engine.get_template(LINK_BINARY)
stamp_template = engine.get_template(LINK_STAMP)


def login(request):
    return render(request, 'login.html')


@login_required
def index(request):
    form = ForexEntryForm()
    return render(request, 'index.html', context={'form': form})


@login_required
def dashboard(request, option):
    if option == 'forex':
        form = ForexEntryForm()
    elif option == 'binary':
        form = BinaryEntryForm()
    else:
        return Http404()
    timestamps = TimeStamp.objects.filter(
        option=option,
        owner=request.user
    )
    context = {
        'form': form, 'option': option,
        't_form': StampForm(
            initial={'option': option, 'owner': request.user.id}),
        "stamps": timestamps,
        'l_form': LessonForm(),
        'r_form': ReasonForm()
    }
    return render(request, 'dashboard.html', context=context)


@api_view(['POST', 'DELETE'])
def stamp(request, id=None):
    if request.method == "POST":
        stamp = StampSerializer(data=request.data)

        if stamp.is_valid():
            stamp.save()
            csrf_token = csrf_token_lazy(request)
            date = parse_date(stamp.data["date"]).strftime('%B %d, %Y')
            context = Context(
                {"stamp": stamp.data, "csrf_token": csrf_token, 'date': date})
            data = dict(
                stamp.data,
                template=stamp_template.render(context=context))
            return Response(data=data)
        return Response(stamp.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            TimeStamp.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TimeStamp.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


def post_wrapper(request, serializer_class, template):
    if request.method == "POST":
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            csrf_token = csrf_token_lazy(request)
            context = Context(
                {"entry": serializer.data, "csrf_token": csrf_token})
            data = dict(
                serializer.data,
                template=template.render(context=context))
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forex(request):
    return post_wrapper(request, ForexSerializer, fx_template)


@api_view(['POST'])
def binary(request):
    return post_wrapper(request, BinarySerializer, binary_template)


def detail_wrapper(request, entry, serializer_class, id):
    try:
        entry = entry.objects.get(entry_id=id)
    except ForexEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = serializer_class(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT'])
def forex_detail(request, id):
    return detail_wrapper(request, ForexEntry, ForexSerializer, id)


@api_view(['DELETE', 'PUT'])
def binary_detail(request, id):
    return detail_wrapper(request, BinaryEntry, BinarySerializer, id)
