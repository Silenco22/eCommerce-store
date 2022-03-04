#able to use in everytemplate
from .models import Category


def categories(request):
    #change .all to .filter(level=0) its django mptt to say where all the root categories are and show only them
    return {
        'categories': Category.objects.filter(level=0)
    }
