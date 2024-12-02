from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
Стандартная парная игра на доверие
"""


class Constants(BaseConstants):
    name_in_url = 'trust_str'
    players_per_group = 2
    num_rounds = 3
    switch_strat = 0

    instructions_template = 'trust_str/instructions.html'
    TotalResult_template = 'trust_str/AdminReport.html'

    endowment = 10
    multiplier = 3


class Subsession(BaseSubsession):
    def get_active_players(self):
        return [p for p in self.get_players()]

    def at_session_start(self):
       self.group_randomly(fixed_id_in_group=True)
       pl_matrix = self.get_group_matrix()
       for row in pl_matrix:
           row.reverse()
       self.set_group_matrix(pl_matrix)


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""Amount sent by P1""", default=0
    )

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""", default=0,
        min=c(0),
    )

    def sent_back_amount_max(self):
        return self.sent_amount * Constants.multiplier

    def set_payoffs(self):
        p = random.randint(1, 2)
        p1 = self.get_player_by_id(p)
        p2 = self.get_player_by_id(3 - p)
        p1.pl_type = 1
        p2.pl_type = 2
        self.sent_amount = p1.q_sent
        self.sent_back_amount = getattr(p2, "q_sent_back_"+str(self.sent_amount))
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplier - self.sent_back_amount


class Player(BasePlayer):
    timeout1 = models.BooleanField(initial=False)
    timeout2 = models.BooleanField(initial=False)
    pl_type = models.IntegerField(min=1, max=2, default=1)

    q_sent = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[i for i in range(11)],
        min=0, max=Constants.endowment
    )

    q_sent_back_0 = models.IntegerField(min=0, max=0, default=0)
    q_sent_back_1 = models.IntegerField(choices=[i for i in range(Constants.multiplier*1+1)], min=0, max=Constants.multiplier*1 )
    q_sent_back_2 = models.IntegerField(choices=[i for i in range(Constants.multiplier*2+1)], min=0, max=Constants.multiplier*2 )
    q_sent_back_3 = models.IntegerField(choices=[i for i in range(Constants.multiplier*3+1)], min=0, max=Constants.multiplier*3 )
    q_sent_back_4 = models.IntegerField(choices=[i for i in range(Constants.multiplier*4+1)], min=0, max=Constants.multiplier*4 )
    q_sent_back_5 = models.IntegerField(choices=[i for i in range(Constants.multiplier*5+1)], min=0, max=Constants.multiplier*5 )
    q_sent_back_6 = models.IntegerField(choices=[i for i in range(Constants.multiplier*6+1)], min=0, max=Constants.multiplier*6 )
    q_sent_back_7 = models.IntegerField(choices=[i for i in range(Constants.multiplier*7+1)], min=0, max=Constants.multiplier*7 )
    q_sent_back_8 = models.IntegerField(choices=[i for i in range(Constants.multiplier*8+1)], min=0, max=Constants.multiplier*8 )
    q_sent_back_9 = models.IntegerField(choices=[i for i in range(Constants.multiplier*9+1)], min=0, max=Constants.multiplier*9 )
    q_sent_back_10 = models.IntegerField(choices=[i for i in range(Constants.multiplier*10+1)], min=0, max=Constants.multiplier*10 )
    
    sent_amount = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""Amount sent by P1""", default=0
    )

    sent_back_amount = models.IntegerField(
        doc="""Amount sent back by P2""", default=0,
        min=0,
    )

    def is_alive(self):
        return not ((self.participant.label is None) or (self.participant.label == ""))

    def role(self):
        return {1: 'A', 2: 'B'}[self.pl_type]
