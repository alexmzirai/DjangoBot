from django.shortcuts import render, get_object_or_404, reverse
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from .parser import parse_intercept_rss
from django.views.generic import View

import telepot

TOKEN = '605347574:AAFLA9YzWE7JnPxK31uCOESsv7X9OSoacrI'	# temporary token key for my bot

AlekiBot = telepot.Bot(TOKEN)

def display_help():
	return render_to_string('help.md')

def display_intercept_feed():
	return render_to_string('feed.md', {'items': parse_intercept_rss()})

class CommandReceiveView(View):
	"""receives post request and handles it appropriately accng to command"""
	def post(self, request, bot_token):
		if bot_token != TOKEN:
			return HttpResponseForbidden('Invalid token')

		commands = {
			'start/': display_help,
			'help': display_help,
			'feed': display_intercept_feed,
		}

		try:
			payload = json.loads(request.body.decode('utf-8'))
		except ValueError:
			HttpResponseBadRequest('invalid request body')
		else:
			chat_id = payload['message']['chat']['id']
			cmd = payload['message'].get('text')
			func = commands.get(cmd.split()[0].lower())
			if func:
				AlekiBot.sendMessage(chat_id, func(), parse_mode='Markdown')
			else:
				AlekiBot.sendMessage(chat_id, 'I do not understand you sir')

		return JsonResponse({}, status=200)


@method_decorator(csrf_exempt)
def dispatch(self, request, *args, **kwargs):
	return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)









