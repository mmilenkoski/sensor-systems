# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .models import Document
from .forms import DocumentForm
from .forms import FileForm
from django.core.files import File
import math
import os
#import matlab.engine

def hello(request):
    return render(
        request,
        'hello.html'
    )

def fileupload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():

            #newdoc = Document(docfile=request.FILES['docfile'])
            #newdoc.save()
            f = request.FILES['docfile']
            with open('test.txt', 'w') as destination:
                for line in f:
                    destination.write(line)
                    destination.write('\n')
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('file'))
            return HttpResponseRedirect(reverse('parameters'))
    else:
        form = FileForm()  # A empty, unbound form
    return render(
        request,
        'fileupload.html',
        {'form': form}
    )


def parameters(request):
    with open('test.txt', 'r') as f:
        first_line = f.readline()
        line = first_line.split(',')
        n = len(line)
    if request.method == 'POST':
        form = DocumentForm(request.POST, n = n)
        if form.is_valid():
            with open('parameters.txt', 'w') as destination:
                for i in range(0, n):
                    l = form.cleaned_data['Lower Bound %s' % (i+1)]
                    u = form.cleaned_data['Upper Bound %s' % (i+1)]
                    s = form.cleaned_data['Step %s' % (i+1)]
                    destination.write(str(l) + ',' + str(u) + ',' + str(s) + '\n')
        return HttpResponseRedirect(reverse('results'))
    else:
        form = DocumentForm(n=n)
    return render(
        request,
        'parameters.html',
        {'form': form, 'size': range(0, n)}
    )

def results(request):

    lowerBounds = []
    upperBounds= []
    steps = []
    with open('parameters.txt', 'r') as destination:
        for line in destination:
            if line in ['\n', '\r\n']:
                continue
            parts = line.split(',')
            parts = [float(x) for x in parts]
            lowerBounds.append(parts[0])
            upperBounds.append(parts[1])
            steps.append(parts[2])
    lista = []
    with open('test.txt', 'r') as destination:
        for line in destination:
            if line in ['\n', '\r\n']:
                continue
            parts = line.split(',')

            parts = [float(x) for x in parts]
            lista.append(parts)




    xvalues = []

    for i in range(0, len(lowerBounds)):
        xvalues.append(getRange(lowerBounds[i], upperBounds[i], steps[i]))

    xtuples = []
    for i in range(0, len(xvalues[0])):
        temp = []
        for j in range(0, len(xvalues)):
            temp.append(round(xvalues[j][i], 4))
        xtuples.append(tuple(temp))

    #print (lista)
    percents = [[], [], [], [],[]]
    mseList = [[], [], [], [],[]]
    rmseList = [[], [], [], [],[]]
    labels = []
    path = os.getcwd()
    #eng = matlab.engine.start_matlab()
    #eng.cd(path)
    for x in xtuples:
        if len(x) == 1:
            labels.append(str(x[0]))
        else:
            labels.append(str(x))
        result1 = previous(lista, x)
        result2 = previous2(lista, x)
        result3 = previous3(lista, x)
        #a = matlab.double(list(x))
        # result4 = eng.lms_vss_mult(3.0, 1, a, nargout=2)
        # result5 = eng.lms_romer_mult(3.0, 1, a, nargout=2)
        #respom = eng.call_script(3.0, 1, a, nargout=4)
        #result4 = [respom[0], respom[1]]
        #result5 = [respom[2], respom[3]]
        percents[0].append(result1[0])
        percents[1].append(result2[0])
        percents[2].append(result3[0])
        #percents[3].append(result4[0])
        #percents[4].append(result5[0])

        mseList[0].append(result1[1])
        mseList[1].append(result2[1])
        mseList[2].append(result3[1])
        #mseList[3].append(result4[1])
        #mseList[4].append(result5[1])

        rmseList[0].append(math.sqrt(result1[1]))
        rmseList[1].append(math.sqrt(result2[1]))
        rmseList[2].append(math.sqrt(result3[1]))
        #rmseList[3].append(math.sqrt(result4[1]))
        #rmseList[4].append(math.sqrt(result5[1]))
    print (mseList[3])
    percents2 = [[], [], [], [],[]]
    mseList2 = [[], [], [], [],[]]
    rmseList2 = [[], [], [], [],[]]
    labels2 = []
    lista = lista[::2]
    for x in xtuples:
        if len(x) == 1:
            labels2.append(str(x[0]))
        else:
            labels2.append(str(x))
        result1 = previous(lista, x)
        result2 = previous2(lista, x)
        result3 = previous3(lista, x)
        #a = matlab.double(list(x))
        # result4 = eng.lms_vss_mult(3.0, 2, a, nargout=2)
        # result5 = eng.lms_romer_mult(3.0, 2, a, nargout=2)
        #respom = eng.call_script(3.0, 1, a, nargout=4)
        #result4 = [respom[0], respom[1]]
        #result5 = [respom[2], respom[3]]
        percents2[0].append(result1[0])
        percents2[1].append(result2[0])
        percents2[2].append(result3[0])
        #percents2[3].append(result4[0])
        #percents2[4].append(result5[0])

        mseList2[0].append(result1[1])
        mseList2[1].append(result2[1])
        mseList2[2].append(result3[1])
        #mseList2[3].append(result4[1])
        #mseList2[4].append(result5[1])

        rmseList2[0].append(math.sqrt(result1[1]))
        rmseList2[1].append(math.sqrt(result2[1]))
        rmseList2[2].append(math.sqrt(result3[1]))
        #rmseList2[3].append(math.sqrt(result4[1]))
        #rmseList2[4].append(math.sqrt(result5[1]))

    return render(
        request,
        'results.html',
        {'percents': percents, 'mseList': mseList, 'rmseList': rmseList,
         'labels': labels, 'percents2': percents2, 'mseList2': mseList2, 'rmseList2': rmseList2,
         'labels2': labels2}
    )

def getRange(l, u, s):
    myrange = []
    i = l
    while i <= u:
        myrange.append(i)
        i += s
        i = round(i, 5)
    return myrange


#comment
def previous(niza, threshold):
    counter = 0
    suma = 0
    for i in range(1, len(niza)):
        flag = False
        tempSuma = 0
        tempList = []
        for j in range(0, len(niza[i])):
            calculation = niza[i-1][j]
            tempList.append(calculation)
            tempSuma += (niza[i][j] - calculation) ** 2
            if math.fabs(niza[i][j]-calculation) > threshold[j]:
                flag = True
                break
        if flag:
            counter += 1
        else:
            suma += tempSuma
            niza[i] = tempList

    return float(counter)/len(niza), float(suma)/len(niza)


def previous2(niza, threshold):
    counter = 0
    suma = 0
    for i in range(2, len(niza)):
        flag = False
        tempSuma = 0
        tempList = []
        for j in range(0, len(niza[i])):
            calculation = (niza[i - 1][j] + niza[i - 2][j]) / 2
            tempList.append(calculation)
            tempSuma += (niza[i][j] - calculation) ** 2
            if math.fabs(niza[i][j]-calculation) > threshold[j]:
                flag = True
                break
        if flag:
            counter += 1
        else:
            suma += tempSuma
            niza[i] = tempList

    return float(counter)/len(niza), float(suma)/len(niza)

def previous3(niza, threshold):
    counter = 0
    suma = 0
    for i in range(3, len(niza)):
        flag = False
        tempSuma = 0
        tempList = []
        for j in range(0, len(niza[i])):
            calculation = (niza[i - 1][j] + niza[i - 2][j] + niza[i - 3][j]) / 3
            tempList.append(calculation)
            tempSuma += (niza[i][j] - calculation) ** 2
            if math.fabs(niza[i][j]-calculation) > threshold[j]:
                flag = True
                break
        if flag:
            counter += 1
        else:
            suma += tempSuma
            niza[i] = tempList

    return float(counter)/len(niza), float(suma)/len(niza)


# def previous2(niza, threshold):
#     counter = 0
#     suma = 0
#     for i in range(2, len(niza)):
#         calculation = (niza[i - 1][0] + niza[i-2][0])/2
#         suma += (niza[i][0] - calculation) ** 2
#         if math.fabs(niza[i][0] - calculation) > threshold[0]:
#             counter += 1
#         else:
#
#             niza[i][0] = calculation
#     return float(counter)/len(niza), float(suma)/len(niza)


# def previous3(niza, threshold):
#     counter = 0
#     suma = 0
#     for i in range(3, len(niza)):
#         calculation = (niza[i - 1][0] + niza[i - 2][0] + niza[i-3][0]) / 3
#         suma += (niza[i][0] - calculation) ** 2
#         if math.fabs(niza[i][0] - calculation) > threshold[0]:
#             counter += 1
#         else:
#
#             niza[i][0] = calculation
#     return float(counter)/len(niza), float(suma)/len(niza)


def mse(niza, threshold):
    current = niza[0]
    counter = 1
    suma = 0
    for i in range(1, len(niza)):
        calculation = niza[i-1]
        suma += (calculation-current)*(calculation-current)

        if math.fabs(current-calculation) > threshold:
            counter += 1
            current = calculation

    return float(suma)/len(niza)


def mse2(niza, threshold):
    current = niza[1]
    counter = 2
    suma = 0
    for i in range(2, len(niza)):
        calculation = (niza[i - 1] + niza[i - 2]) / 2
        suma += (calculation-current)*(calculation-current)

        if math.fabs(current-calculation) > threshold:
            counter += 1
            current = calculation

    return float(suma)/len(niza)


def mse3(niza, threshold):
    current = niza[2]
    counter = 3
    suma = 0
    for i in range(2, len(niza)):
        calculation = (niza[i - 1] + niza[i - 2] + niza[i-3]) / 3
        suma += (calculation-current)*(calculation-current)

        if math.fabs(current-calculation) > threshold:
            counter += 1
            current = calculation

    return float(suma)/len(niza)

def document(request):
    return HttpResponseRedirect(reverse('file'))
    print (2)
    # Handle file upload
    if request.method == 'POST' and 'sbmButton' in request.POST:
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            flag = True
            #newdoc = Document(docfile=request.FILES['docfile'])
            #newdoc.save()
            l = form.cleaned_data['lower']
            u = form.cleaned_data['upper']
            s = form.cleaned_data['step']
            with open('parameters.txt', 'w') as destination:
                destination.write(str(l)+'\n')
                destination.write(str(u)+'\n')
                destination.write(str(s)+'\n')
            f = request.FILES['docfile']
            with open('test.txt', 'w') as destination:
                for line in f:
                    destination.write(line)


            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
            #return HttpResponseRedirect(reverse('parameters'))
    else:
        form = DocumentForm()  # A empty, unbound form
    with open('parameters.txt', 'r') as destination:
        l = float(destination.readline())
        u = float(destination.readline())
        s = float(destination.readline())

    list = []
    with open('test.txt', 'r') as destination:
        for line in destination:
            line = line.split(',')
            for i in line:
                list.append(float(i))

    mseList = [[], [], []]
    rmseList = [[], [], []]
    labels = []
    i = l
    while i <= u:
        labels.append(float("{0:.2f}".format(i)))
        mseList[0].append(mse(list, i))
        mseList[1].append(mse2(list, i))
        mseList[2].append(mse3(list, i))
        rmseList[0].append(math.sqrt(mse(list, i)))
        rmseList[1].append(math.sqrt(mse2(list, i)))
        rmseList[2].append(math.sqrt(mse3(list, i)))
        i += s

    percents = [[], [], []]
    labels = []
    i = l
    while i <= u:
        labels.append(float("{0:.2f}".format(i)))
        percents[0].append(previous(list, i))
        percents[1].append(previous2(list, i))
        percents[2].append(previous3(list, i))
        i += s

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form, 'percents': percents, 'mseList': mseList, 'rmseList': rmseList,
         'labels': labels}
    )

