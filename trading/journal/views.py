from django.shortcuts import render
from .forms import ForexEntryForm, BinaryEntryForm, StampForm
from .models import ForexEntry, BinaryEntry, TimeStamp
from .serializers import StampSerializer, BinarySerializer, ForexSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import Context, engines
from django.template.backends.utils import csrf_token_lazy
from django.utils.dateparse import parse_date


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
    t_form = StampForm(initial={'option': option, 'owner': request.user.id})
    return render(
        request, 'dashboard.html',
        context={
            'form': form, 'option': option, 't_form': t_form,
            "stamps": timestamps
        })


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
            template = stamp_template.render(context=context)
            s = dict(stamp.data)
            s.update({"template": template})
            return Response(data=s)
        return Response(stamp.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            stamp = TimeStamp.objects.get(id=id)
            stamp.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TimeStamp.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def forex(request):
    if request.method == "POST":
        serializer = ForexSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            csrf_token = csrf_token_lazy(request)
            context = Context(
                {"entry": serializer.data, "csrf_token": csrf_token})
            template = fx_template.render(context=context)
            print(serializer.data)
            s = dict(serializer.data)
            s.update({"template": template})
            return Response(data=s)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def binary(request):
    if request.method == "POST":
        serializer = BinarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            csrf_token = csrf_token_lazy(request)
            context = Context(
                {"entry": serializer.data, "csrf_token": csrf_token})
            template = binary_template.render(context=context)
            print(serializer.data)
            s = dict(serializer.data)
            s.update({"template": template})
            return Response(data=s)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT'])
def forex_detail(request, id):
    try:
        entry = ForexEntry.objects.get(entry_id=id)
    except ForexEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ForexSerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT'])
def binary_detail(request, id):
    try:
        entry = BinaryEntry.objects.get(entry_id=id)
    except BinaryEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = BinarySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def stamp_delete(request, pk):
    pass
