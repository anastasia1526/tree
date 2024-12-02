from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class StartWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.subsession.at_session_start()

class Introduction(Page):
   timeout_seconds = 60
   is_first_round_show = True
   def is_enabled(self):
       return (self.round_number == 1)


class Send(Page):

    timeout_seconds = 120
    form_model = 'player'
    form_fields = ['q_sent']

    def set_bot_decision(self):
        self.player.q_sent = Constants.endowment
    def before_next_page(self):
        if self.timeout_happened:
            self.set_bot_decision()
            self.player.timeout1 = True

class SendBack(Page):

    timeout_seconds = 120
    form_model = 'player'
    form_fields = ['q_sent_back_'+str(i+1) for i in range(10)]

    def vars_for_template(self):
        return dict(
            sendA=[i for i in range(11)],
            capB=[i*Constants.multiplier for i in range(11)],
            flds=self.form_fields
        )

    def set_bot_decision(self):
        self.player.q_sent_back_1 = Constants.multiplier*1
        self.player.q_sent_back_2 = Constants.multiplier*2
        self.player.q_sent_back_3 = Constants.multiplier*3
        self.player.q_sent_back_4 = Constants.multiplier*4
        self.player.q_sent_back_5 = Constants.multiplier*5
        self.player.q_sent_back_6 = Constants.multiplier*6
        self.player.q_sent_back_7 = Constants.multiplier*7
        self.player.q_sent_back_8 = Constants.multiplier*8
        self.player.q_sent_back_9 = Constants.multiplier*9
        self.player.q_sent_back_10 = Constants.multiplier*10
    def before_next_page(self):
        if self.timeout_happened:
            self.set_bot_decision()
            self.player.timeout2 = True


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    title_text = "Пожалуйста, подождите"
    body_text = "Ожидайте пока Ваш оппонент примет решение."
    def after_all_players_arrive(self):
        for p in self.subsession.get_groups():
            p.set_payoffs()


class Results(Page):
    timeout_seconds = 40      
    """This page displays the earnings of each player"""
    def vars_for_template(self):
        return dict(
            tripled_amount=self.group.sent_amount * Constants.multiplier
        )


page_sequence = [
    StartWaitPage,
    Introduction,
    Send,SendBack,
    ResultsWaitPage,
    Results
]
