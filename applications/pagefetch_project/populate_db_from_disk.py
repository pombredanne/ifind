#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   27/10/2013

Requires:
---------
"""
import sys
from django.core.management import setup_environ
from pagefetch_project import settings
setup_environ(settings)

from ifind.models.game_models import Page
from ifind.common.utils import get_trending_queries
from ifind.models import game_model_functions

from ifind.models.game_model_functions import populate


from configuration import  STATIC_PATH
import os


def populate_cats():
    game_model_functions.get_category('Space objects', 'cat_images/spooky-space-halloween-little-ghost-nebula_42686_600x450.jpg','',append=True)
    game_model_functions.get_category('Actors', 'cat_images/forbes-highest-paid-celebrities-05.jpg','',append=True)
    game_model_functions.get_category('Musical Artists','cat_images/thekooks-music-box.jpg','',append=True)
    game_model_functions.get_category('Films', 'cat_images/films-2013-dispicable-me-2.jpg','',append=True)
    game_model_functions.get_category('Games', 'cat_images/download.jpeg','',append=True)
    game_model_functions.get_category('Kids TV', 'cat_images/jamie.jpg','',append=True)
    game_model_functions.get_category('Business People', 'cat_images/gekko.jpg','',append=True)
    game_model_functions.get_category('Universities', 'cat_images/glasgow_uni_200382a1.jpg','',append=True)




def main():
    populate_cats()
    #split line into tokens
    meta_data_file = sys.argv[1]
    data_list = get_trending_queries(meta_data_file)
    for data_tuple in data_list:
        cat = game_model_functions.get_category(data_tuple[0],'icon','',append=True)
        p = Page(category=cat, title=data_tuple[2], is_shown=True, url=data_tuple[1], screenshot=data_tuple[3])
        p.save()
    return 0


if __name__ == "__main__":
    sys.exit(main())