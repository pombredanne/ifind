""" Avatar Message Service -- Taking in UserProfile, HighSchores, CurrentGame & CurrentPage"""

import sys
import random
import inspect
import pprint as pp

DEBUG = True

####################
# CONTEXT HANDLERS #
####################

# Pages

INDEX = "IndexPage"
CATEGORY = 'CategoryPage'
GAME = 'GamePage'
GAME_OVER = 'GameOverPage'

# Ajax

SEARCH = 'Search'

HANDLERS = (INDEX,
            CATEGORY,
            GAME,
            GAME_OVER,
            SEARCH)


class Handler(object):
    """
    Abstract class representing a site page.
    Each instance encapsulates a page's potential responses & related logic.

    """
    def __init__(self, context, user=None, current_game=None):

        self.context = context
        self.user = user
        self.current_game = current_game
        self.logged_in = True if user else False

    def get_message(self):
        """
        Public API to be used by GameAvatar.

        """
        if DEBUG:
            print
            pp.pprint(vars(self))
            print

        if self.logged_in:
            return self._get_user_message()
        elif not self.logged_in:
            return self._get_anonymous_message()

    def _get_anonymous_message(self):
        """
        Abstract method for anonymous message logic.

        """
        pass

    def _get_user_message(self):
        """
        Abstract method for user message logic.

        """
        pass


class IndexPage(Handler):
    """
    Page handler implementation of Index Page

    """

    UNIVERSALS = ["Fancy a game?",
                  "Play a game!",
                  "Go for it!"]

    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game=None

        messages = ["Why don't you try a game?",
                    "Check out how to play!",
                    "Have you registered an account yet?",
                    "Welcome to Retrieve Me if You Can!"]

        messages += self.UNIVERSALS

        return random.choice(messages)

    def _get_user_message(self):

        # Assumptions: user, current_game=None

        # "Fancy a game?"
        # "You've played X games, why not try another?"
        # "You're so close to achieving X achievement!"
        # "You've not logged in for ages :("
        # "You're around these parts pretty often!"
        # "Checked out your profile lately?"
        # "You're currently ranked Xth. You can do better!"

        messages = []

        return "I am logged in and at index page"


class CategoryPage(Handler):
    """
    Page handler implementation of Category Page

    """

    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game=None

        # "If you log in/register you can see your high scores for every category!"
        # "Pick a category!"

        messages = ["Pick a category!",
                    "The first one looks good...",
                    "Log in to see your high scores for each category!",
                    "Choose a category!"]

        return random.choice(messages)

    def _get_user_message(self):

        # Assumptions: user, current_game=None

        # "Pick a category!"
        # "You've not played any games in X category!"
        # "You've played A LOT of games in X category!"
        # "Been ages since you played!"

        return "Pick a category"


class GamePage(Handler):
    """
    Page handler implementation of a Game Page (when playing)

    """

    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game

        return "Anonymous dude is starting.."

    def _get_user_message(self):

        # Assumptions: user, current_game

        return "Authorised legit dude is starting..."


class Search(Handler):
    """
    Handler implementation of a Search query AJAX request.

    """
    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game

        return "Anonymous dude has searched!"

    def _get_user_message(self):

        # Assumptions: user, current_game

        return "Authorised legit dude has searched!"





class GameAvatar (object):

    def __init__(self, context=None, user=None, current_game=None):

        self.context = context
        self.user = user
        self.current_game = current_game

        if context:
            self._handler = self._get_handler(context, user, current_game)

    def get(self):
        """
        Returns message within context of GameAvatar's arguments.

        Usage:
            avatar = GameAvatar(arg1, arg2, etc)
            avatar.send()

        """
        return self._handler.get_message()

    def update(self, context=None, user=None, current_game=None):
        """
        Update critical GameAvatar attributes, arguments are flexibly optional.

        Usage:
            avatar = GameAvatar(arg1)
            avatar.send()
            avatar.update(arg2)
            avatar.send()

        """
        if context is not None:
            self.page = context

        if user is not None:
            self.user = user

        if current_game is not None:
            self.current_game = current_game

        self._handler = self._get_handler(self.context, self.user, self.current_game)

    def _get_handler(self, context, *args):
        """
        Instantiate and return appropriate page handler using instance page attribute.

        """
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if obj.__name__ == context:
                    return obj(context, *args)