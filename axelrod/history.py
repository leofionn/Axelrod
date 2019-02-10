from collections import Counter, defaultdict

from axelrod.action import Action, actions_to_str

C, D = Action.C, Action.D


class HistoryList(object):
    # def __init__(self, history=None, shared=False):
    #     self.shared = shared
    def __init__(self, history=None):
        self._history = []
        self._counter = Counter()
        # Broken, needs to be on Joint History
        self.state_distribution = defaultdict(int)
        if isinstance(history, History):
            history = history._history
        if history:
            # if shared:
            #     self._history = history
            # else:
            self.extend(history)
        self._len = len(self._history)

    def append(self, play, opp_play=None):
        # self._len += 1
        self._history.append(play)
        self._counter[play] += 1
        if opp_play:
            self.state_distribution[(play, opp_play)]

    @property
    def cooperations(self):
        return self._counter[C]

    def copy(self):
        # new_history = History(history=self._history, shared=self.shared)
        new_history = History(history=self._history)
        return new_history

    @property
    def defections(self):
        return self._counter[D]

    def extend(self, plays):
        for play in plays:
            self.append(play)

    def pop(self, index):
        play = self._history.pop(index)
        self._counter[play] -= 1
        # self._len -= 1
        return play

    def reset(self):
        self._history = []
        self.state_distribution = defaultdict(int)
        # self._len = 0
        self._counter = Counter()

    def __eq__(self, other):
        # Allow comparison to lists and strings
        if isinstance(other, list):
            # other_history = "".join(other)
            other_history = other
        # elif isinstance(other, str):
        #     # other_history = other
        #     other_history = list(other)
        elif isinstance(other, HistoryList):
            other_history = other._history
        else:
            print(other)
            raise ValueError("Cannot compare types.")
        ## Need to also check state distribution?
        return self._history == other_history

    def __add__(self, other):
        if isinstance(other, list):
            # temp = self._history + ''.join(other)
            temp = self._history + other
        elif isinstance(other, str):
            temp = self._history + list(other)
        elif isinstance(other, HistoryList):
            temp = self._history + other._history
        return HistoryList(temp)

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return self._history[key]

    def __str__(self):
        return actions_to_str(self._history)

    def __list__(self):
        return self._history

    def __len__(self):
        # return self._len
        return len(self._history)

    def __repr__(self):
        return "History: {}".format(actions_to_str(self._history))


class HistoryString(object):
    def __init__(self, history=None):
        self._history = ""
        self._len = 0
        self._counter = Counter()
        if isinstance(history, History):
            history = history._history
        if history:
            self.extend(history)

    def append(self, play):
        self._history += actions_to_str(play)
        self._counter[play] += 1
        self._len += 1

    @property
    def cooperations(self):
        return self._counter[C]

    def copy(self):
        new_history = History(self._history)
        return new_history

    @property
    def defections(self):
        return self._counter[D]

    def extend(self, plays):
        for play in plays:
            self.append(play)

    def pop(self, index):
        if index == -1:
            index = len(self._history) - 1
        play = self._history[index]
        self._history = self._history[:index] + self._history[index+1:]
        self._counter[play] -= 1
        self._len -= 1
        return play

    def reset(self):
        self._history = ""
        self._counter = Counter()
        self._len = 0

    def __add__(self, other):
        if isinstance(other, HistoryString):
            temp = self._history + other._history
        elif isinstance(other, str):
            temp = self._history + other
        elif isinstance(other, list):
            temp = self._history + ''.join(other)
        return HistoryString(temp)

    def __eq__(self, other):
        # Allow comparison to lists and strings
        if isinstance(other, HistoryString):
            other_history = other._history
        elif isinstance(other, str):
            other_history = other
        elif isinstance(other, list):
            other_history = "".join(other)
        else:
            raise ValueError("Cannot compare types.")

        return self._history == other_history

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return list(self._history[key])

    def __str__(self):
        return self._history

    def __list__(self):
        return list(self._history)

    def __len__(self):
        return self._len
        # return len(self._history)

    def __repr__(self):
        return "History: {}".format(actions_to_str(self._history))


History = HistoryList


class JointHistory(object):
    def __init__(self, my_history, op_history):
        self._my_history = History(my_history)
        self._op_history = History(op_history)
        self._joint = defaultdict(int)
        for (h1, h2) in zip(my_history, op_history):
            self._joint[(h1, h2)] += 1

    def append(self, my_play, op_play):
        self._my_history.append(my_play)
        self._op_history.append(op_play)
        self._joint[(my_play, op_play)] += 1

    # def cooperations(self):
    #     return self._my_history.cooperations()

    def copy(self):
        new = JointHistory(self._my_history, self._op_history)
        return new

    # def defections(self):
    #     return self._my_history.defections()

    def pop(self, index):
        my_play = self._my_history.pop(index)
        op_play = self._my_history.pop(index)
        self._joint[(my_play, op_play)] -= 1
        return my_play, op_play

    def reset(self):
        self._my_history.reset()
        self._op_history.reset()
        self._joint = Counter()

    def __eq__(self, other):
        return (self._my_history == other._my_history) and \
               (self._op_history == other._op_history)

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return self._my_history[key], self._op_history[key]

    def __len__(self):
        return len(self._my_history)


