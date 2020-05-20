import sys
import readline
from time import time
from datetime import datetime
from os import path
from ._votingclient import Error

class CLI:

    def __init__ (self, voting_client):
        self._vc = voting_client

    def _error (self, message):
        sys.stderr.write('Error: ' + message + '\n')

    def _input (self, prompt, buf=None, required=True):
        while True:
            if buf is not None:
                readline.set_startup_hook(lambda: readline.insert_text(buf))
            line = input(prompt)
            readline.set_startup_hook()
            if required and not line:
                continue
            return line

    def _read_date (self, prompt, date):
        text = date
        while True:
            text = self._input(prompt, text)
            try:
                datetime.fromisoformat(text)
                return text
            except:
                self._error('Invalid date. Please retry.')

    def _date_text2ts (self, text_date):
        return int(datetime.timestamp(datetime.fromisoformat(text_date)))

    def _date_ts2text (self, ts):
        text = datetime.isoformat(datetime.fromtimestamp(ts))
        return text.replace('T', ' at ')

    def create_vote (self, title=None, closing=None, expiry=None,
                     propositions=[]):
        title = self._input('> Title: ', title)
        print('Dates have to be entered using the YYYY-MM-DD HH:MM format.')
        closing = self._read_date('> Closing date: ', closing)
        expiry = self._read_date('> Expiring date: ', expiry)
        print('> Propositions (one by line, end with a blank line):')
        while True:
            new_propositions = []
            while True:
                prop = propositions[len(new_propositions)] \
                    if len(propositions) > len(new_propositions) else None
                proposition = self._input('- ', prop, False)
                if not proposition:
                    break
                new_propositions.append(proposition)
            if not new_propositions:
                self._error('A vote needs at least one proposition.')
                continue
            propositions = new_propositions
            break
        print('\nOK. Summary of your vote:')
        print('  Title: ' + title)
        print('  Closing on: ' + closing)
        print('  Expiring on: ' + expiry)
        print('  Propositions:')
        for proposition in propositions:
            print('  - ' + proposition)
        if input('> Is this ok? ([y]es/[N]o) ').lower() == 'y':
            try:
                self._vc.create_vote(title,
                                     self._date_text2ts(closing),
                                     self._date_text2ts(expiry),
                                     propositions)
                print('Vote successfully created!')
                vote_file = 'secret.thc'
                if path.exists(vote_file):
                    n = 1
                    while path.exists('secret' + str(n) + '.thc'):
                        n += 1
                    vote_file = 'secret' + str(n) + '.thc'
                if not self._vc.export_vote(vote_file):
                    self._error('Could not save vote to file. Dumping vote:')
                    print(self._vc.dump_vote())
                else:
                    print('Successfully saved vote to ' + vote_file + '.')
                return 0
            except Error as e:
                self._error(e.message)
                return 1
        else:
            if input('> What to do? [e]dit/[A]bandon ').lower() == 'e':
                return self.create_vote(title, closing, expiry, propositions)

    def _list_propositions (self):
        print('\nPropositions:')
        for i in range(len(self._info['propositions'])):
            print('  ' + str(i + 1) + '- ' + self._info['propositions'][i])

    def _ask_votes (self, name):
        print('\nPlease enter votes for ' + name + ':')
        ballot = []
        for i in range(len(self._info['propositions'])):
            while True:
                votes = self._input('> How many votes for proposition ' +
                                    str(i + 1) + '? ')
                if not votes.isdigit():
                    self._error('You must enter a number.')
                else:
                    ballot.append(int(votes))
                    break
        return ballot

    def _list_ballots (self):
        try:
            self._ballots = self._vc.get_ballots()
        except Error as e:
            self._error(e.message)
            return 1
        print('\nBallots list:')
        for ballot in self._ballots:
            print('  - ' + ballot['author'] + ' ', end='')
            if ballot['count'] is False:
                print('has an invalid vote count.')
            else:
                print('exprimed ' + str(ballot['count']) + ' votes in total.')

    def _show_results (self):
        try:
            results = self._vc.get_results(self._ballots)
        except Error as e:
            self._error(e.message)
            return 1
        print('\nVote results:')
        for result in results:
            print('  - ' + result['proposition'] + ': ', end='')
            if result['score'] is False:
                print('invalid vote count')
            else:
                print(str(result['score']))

    def _menu_open (self):
        while True:
            print('\nYou can:')
            print('1- see the [l]ist of [p]ropostions')
            print('2- submit a [b]allot / cast a [v]ote')
            print('3- [e]xit')
            action = self._input('> ').lower()
            if action in ('1', 'l', 'p'):
                self._list_propositions()
            elif action in ('2', 'b', 'v'):
                print('')
                author = self._input('> Participant name? ')
                self._list_propositions()
                ballot = self._ask_votes(author)
                try:
                    self._vc.cast_ballot(author, ballot)
                    print('Ballot successfully cast.')
                except Error as e:
                    self._error(e.message)
                    return 1
            elif action in ('3', 'e'):
                return 0
            else:
                self._error('Invalid command.')

    def _menu_closed (self):
        self._ballots = None
        while True:
            print('\nYou can:')
            print('1- [l]ist [b]allots')
            print('2- [s]how and verify vote [r]esults')
            print('3- [e]xit')
            action = self._input('> ').lower()
            if action in ('1', 'l', 'b'):
                self._list_ballots()
            elif action in ('2', 's', 'r'):
                self._show_results()
            elif action in ('3', 'e'):
                return 0
            else:
                self._error('Invalid command.')

    def main (self):
        try:
            self._info = self._vc.get_info()
        except Error as e:
            self._error(e.message)
            return 1
        print('Vote title: ' + self._info['title'])
        if self._info['closing'] > time():
            print('This vote is open until the ' +
                  self._date_ts2text(self._info['closing']))
            self._menu_open()
        else:
            print('This vote is closed since the ' +
                  self._date_ts2text(self._info['closing']))
            self._menu_closed()
        print('\nBye :).')
        return 0
