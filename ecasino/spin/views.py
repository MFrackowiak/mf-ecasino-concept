from django.shortcuts import render
from django.views.generic import TemplateView


class PlaySpinsView(TemplateView):
    template_name = 'spin/spin.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
