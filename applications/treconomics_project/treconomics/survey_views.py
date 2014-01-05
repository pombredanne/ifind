__author__ = 'leif'

# Can access them all methods but they need to be prefaced with os or datetime for example
import os
import datetime
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from experiment_functions import get_experiment_context
from experiment_functions import log_event


from models_experiments import DemographicsSurvey, DemographicsSurveyForm
from models_experiments import PreTaskTopicKnowledgeSurvey, PreTaskTopicKnowledgeSurveyForm
from models_experiments import PostTaskTopicRatingSurvey, PostTaskTopicRatingSurveyForm
from models_experiments import NasaSystemLoad, NasaSystemLoadForm
from models_experiments import NasaQueryLoad, NasaQueryLoadForm
from models_experiments import NasaNavigationLoad, NasaNavigationLoadForm
from models_experiments import NasaAssessmentLoad, NasaAssessmentLoadForm
from models_experiments import NasaFactorCompare, NasaFactorCompareForm
from models_experiments import SearchEfficacy, SearchEfficacyForm

@login_required
def view_search_efficacy_survey( request ):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = SearchEfficacyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="SELF_SEARCH_EFFICACY_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = SearchEfficacyForm(request.POST)
    else:
        log_event(event="SELF_SEARCH_EFFICACY_SURVEY_STARTED", request=request)
        survey = SearchEfficacyForm()

    action = '/treconomics/searchefficacysurvey/'
    return render_to_response("survey/search_efficacy_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)

@login_required
def view_demographics_survey( request ):
    context = RequestContext(request)
    #uname = request.user.username
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = DemographicsSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="DEMOGRAPHICS_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = DemographicsSurveyForm(request.POST)
    else:
        log_event(event="DEMOGRAPHICS_SURVEY_STARTED", request=request)
        survey = DemographicsSurveyForm()

    action = '/treconomics/demographicssurvey/'
    return render_to_response("survey/demographics_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)



@login_required
def view_nasa_load_survey( request ):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = NasaSystemLoadForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="NASA_LOAD_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = NasaSystemLoadForm(request.POST)
    else:
        log_event(event="NASA_LOAD_SURVEY_STARTED", request=request)
        survey = NasaSystemLoadForm()

    action = '/treconomics/nasaloadsurvey/'
    return render_to_response("survey/nasa_load_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)


@login_required
def view_nasa_query_load_survey( request ):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = NasaQueryLoadForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="NASA_QUERY_LOAD_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = NasaQueryLoadForm(request.POST)
    else:
        log_event(event="NASA_QUERY_LOAD_SURVEY_STARTED", request=request)
        survey = NasaQueryLoadForm()

    action = '/treconomics/nasaqueryloadsurvey/'
    return render_to_response("survey/nasa_query_load_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)


@login_required
def view_nasa_navigation_load_survey( request ):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = NasaNavigationLoadForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="NASA_NAVIGATION_LOAD_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = NasaNavigationLoadForm(request.POST)
    else:
        log_event(event="NASA_NAVIGATION_LOAD_SURVEY_STARTED", request=request)
        survey = NasaNavigationLoadForm()

    action = '/treconomics/nasanavigationloadsurvey/'
    return render_to_response("survey/nasa_navigation_load_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)



@login_required
def view_nasa_assessment_load_survey( request ):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = NasaAssessmentLoadForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="NASA_ASSESSMENT_LOAD_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = NasaAssessmentLoadForm(request.POST)
    else:
        log_event(event="NASA_ASSESSMENT_LOAD_SURVEY_STARTED", request=request)
        survey = NasaAssessmentLoadForm()

    action = '/treconomics/nasaassessmentloadsurvey/'
    return render_to_response("survey/nasa_assessment_load_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)


@login_required
def view_nasa_factor_compare_survey( request ):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = NasaFactorCompareForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event="NASA_COMPARE_FACTORS_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = NasaFactorCompareForm(request.POST)
    else:
        log_event(event="NASA_COMPARE_FACTORS_SURVEY_STARTED", request=request)
        survey = NasaFactorCompareForm()

    action = '/treconomics/nasafactorcomparesurvey/'
    return render_to_response("survey/nasa_factor_compare_survey.html", {'participant': uname, 'condition': condition, 'formset': survey, 'action': action   }, context)
