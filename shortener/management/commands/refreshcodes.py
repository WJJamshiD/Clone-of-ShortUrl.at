from django.core.management.base import BaseCommand, CommandError
from shortener.models import WjUrl
from shortener.utils import generate_shortcode

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int,help='Number of url which must have refresh shortcodes.')

        parser.add_argument(
            '--size',
            type=int,
        )

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete  instead of refreshing shortcodes.',
        )

    def handle(self, *args, **options):
            qs = WjUrl.objects.filter(id__gte=1)[:options['number']]
            if options['delete']:
                for url in qs:
                    print(url.shortcode,end='|')
                    url.delete()
                    print('deleted')
            else:
                WjUrl.objects.refresh_shortcodes(number=options['number'],size=options['size']) 


            

