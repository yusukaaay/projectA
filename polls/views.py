# -*- coding: utf-8 -*-
from django.core.context_processors import request, csrf
from django.http import HttpResponse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import loader
from django.template.context import Context
from polls.models import Poll, Choice
from django.core.urlresolvers import reverse

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    # output = ', '.join([p.question for p in latest_poll_list])
    return render_to_response('polls/index.html',
                              {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    c = {}
    c.update(csrf(request))
    try:
        p = Poll.objects.get(pk=poll_id)
        c.update({'poll': p})
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response("polls/detail.html", c)

def vote(request, poll_id):
    c = {}
    c.update(csrf(request))
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Poll 投票フォームを再表示します。
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "選択肢を選んでいません。",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # ユーザが Back ボタンを押して同じフォームを提出するのを防ぐ
        # ため、POST データを処理できた場合には、必ず
        # HttpResponseRedirect を返すようにします。
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})
