from .forms import EmailForm


def subscribe_form(request):
    return {'form': EmailForm()}
