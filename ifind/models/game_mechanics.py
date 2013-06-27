__author__ = 'leif'

from game_models import CurrentGame, Page, Category
from random import randint
from game_model_functions import get_page_list, set_page_list
from ifind.utils.rotation_ordering import RotationOrdering
#from datetime import datetime

MAX_SCORE = 1000
MAX_QUERIES = 20
MAX_PAGES = 4
MAX_QUERIES_PER_PAGE = 5
GAME_LENGTH_IN_SECONDS = 0


class GameMechanic(object):

    def __init__(self, search_engine=None):
        """
        :return: GameMechanic object
        """
        self.game = None
        self.search_engine = search_engine



    def create_game(self, user, cat, game_type=0):
        """ create a new game for the user given the category
        set the cu
        :param user: User object
        :param cat: models.Category object
        :param pages: records from model.Page given cat
        :return: None
        """

        self.game = CurrentGame(user=user, category=cat)
        #set starting values for game
        # get the pages associated with the category (cat)
        self.set_pages_to_use(game_type)
        #set starting page order for game
        self.generate_page_ordering()
        # now set the first page to find in the game
        self.set_next_page()
        # save to db
        self.update_game()


    def retrieve_game(self, user, game_id):
        """ find the game associated with this user, and return the
            record from ifind.models.game_models.CurrentGame
        :param user:
        :param game_id:
        :return: True, if game is found, else False, if not
        """

        self.game = None
        found = False
        # look up model for game_id

        # try except here?
        cg = CurrentGame.objects.get(id=game_id)
        # if found, set self.game to game record
        if cg:
            self.game = cg
            self.set_pages_to_use(game_type)
            found = True

        return found


    def is_game_over(self):
        """ checks if the game is over
        :param game:
        :return: True if the end game criteria have been met, else False
        """
        # example criteria for the game end
        print 'round: %d max-pages: %d' % (self.get_round_no(),MAX_PAGES)
        if (self.get_round_no() > MAX_PAGES):
            return True
        else:
            return False

    def get_round_no(self):
        return self.game.no_rounds+1

    def get_max_rounds(self):
        return MAX_PAGES

    def _increment_queries_issued(self, query_successful=False):
        self.game.no_of_queries_issued += 1
        self.game.no_of_queries_issued_for_current_page += 1
        if query_successful:
            self.game.no_of_successful_queries_issued +=1

    def _increment_round(self, round_successful=False):
        self.game.no_rounds += 1
        if round_successful:
            self.game.no_rounds_completed += 1

    def _increment_score(self, points=0):
        self.game.current_score += points

    def update_game(self):
        """ make updates to game then save to db
        :param game:
        :return: None
        """
        self.game.save()

    def set_pages_to_use(self, game_type):
        """ select a bunch of pages given the category and the game type
        :param game_type:
        :return: None
        """
        self.pages = Page.objects.filter(category=self.game.category)
        print 'number of pages: %d' % (len(self.pages))
        #todo(leifos): check the number of pages does exceed MAX_PAGES

    def generate_page_ordering(self):
        """ given the list self.pages, create the ordering of pages for the game
        :param pages:
        :return:
        """
        # use the RotationOrdering class to gen the ordering
        ro = RotationOrdering()
        print self.pages
        page_list = ro.get_ordering(self.pages)
        # set the page_list to the the game
        print "page ordering"
        print page_list
        set_page_list(self.game, page_list)


    def set_next_page(self):
        """
        :return: True if next page is set, else False
        """
        # from game get the page_list

        page_list = get_page_list(self.game)
        l = len(page_list)
        # given the round, select the page_id from page_list

        r = self.game.no_rounds

        if r < l:
            page_id = page_list[r]
            print r, page_id
        else:
            return False
        # associate the page from the page model to game
        try:
            self.game.current_page = self.pages.get(id=page_id)
            return True
        except:
            self.game.current_page = None
            return False

    def take_points(self):
        success = False
        if self.game.last_query_score > 0:
            self._increment_score(self.game.last_query_score)
            success = True
        self._increment_round(success)

        self.game.last_query_score = 0
        self.game.last_query = ''
        # increment round here ?????

    def handle_query(self, query):
        score = self._score_query(query)
        self.game.last_query = query
        self.game.last_query_score = score
        print 'query: %s got %d points' % (query, score)
        # increment query here ????
        success = False
        if score > 0:
            success = True
        self._increment_queries_issued(success)

    def _score_query(self, query):
        """sends query to the search engine, checks if the page is returned,
           assign score to page, based on the rank
        :param query_terms: string
        :param url_to_find: string
        :return: integer
        """

        results = self._run_query( query)
        rank = self._check_result(results)
        score = self._score_rank(rank)
        return score

    def _run_query(self, query):
        """ constructs ifind.search.query, and issues it to the search_engine

        :param query:
        :return: ifind.search.response
        """

        # issue query to self.search_engine
        return True

    def _check_result(self, response):
        """ iterates through the response looking for what rank the url is at

        :param response: ifind.search.response
        :param url_to_find: url string
        :return: rank of the url if found, else 0
        """
        url_to_find = self.game.current_page
        # is url_to_fin in response??
        return randint(0,10)


    def _score_rank(self, rank):
        """
        calculates the score based on the rank of the page
        :param rank: integer
        :return: integer
        """
        score = 0
        if rank > 0:
            score = round(MAX_SCORE / rank, 0)

        return score

    def get_last_query_score(self):
        return self.game.last_query_score

    def get_last_query(self):
        return self.game.last_query


    def __str__(self):
        if self.game:
            return 'Game %d - Current Score: %d for ' \
                   'user: %s \nPlaying category: %s round: %d  queries issued: %d \n' \
                   '\nPage to find: %s' \
                   % (self.game.id, self.game.current_score, self.game.user, self.game.category, self.get_round_no(), self.game.no_of_queries_issued, self.game.current_page)

        else:
            return 'Unitialised Game'



