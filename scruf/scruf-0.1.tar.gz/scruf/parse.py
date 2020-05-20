import enum

from scruf import exception, test


class _Tokeniser(object):
    COMMENT_CHARACTER = "#"
    INDENT = "    "
    COMMAND_CHARACTER = "$"
    CONTINUE_CHARACTER = ">"
    COMMAND_PREFIX = INDENT + COMMAND_CHARACTER
    CONTINUE_PREFIX = INDENT + CONTINUE_CHARACTER

    @classmethod
    def is_command(self, line):
        return line.startswith(self.COMMAND_PREFIX)

    @classmethod
    def is_continue(self, line):
        return line.startswith(self.CONTINUE_PREFIX)

    @classmethod
    def is_description(self, line):
        return not line[0].isspace() and not self.is_comment(line)

    @classmethod
    def is_comment(self, line):
        return line.startswith(self.COMMENT_CHARACTER)

    @classmethod
    def is_empty(self, line):
        return not line or not line.startswith(self.INDENT) and line.isspace()

    @classmethod
    def is_result(self, line):
        return (
            line.startswith(self.INDENT)
            and not self.is_command(line)
            and not self.is_continue(line)
        )

    @classmethod
    def get_command(self, line):
        return line[len(self.COMMAND_PREFIX) :].strip()

    @classmethod
    def get_continue(self, line):
        return line[len(self.CONTINUE_PREFIX) :].strip()

    @classmethod
    def get_description(self, line):
        return line

    @classmethod
    def get_result(self, line):
        return line[len(self.INDENT) :]


class _FSM(object):
    class States(enum.Enum):
        START = enum.auto()
        DESCRIPTION = enum.auto()
        COMMAND = enum.auto()
        CONTINUE = enum.auto()
        RESULT = enum.auto()

    STATE_NAMES = {
        States.START: "start",
        States.DESCRIPTION: "description",
        States.COMMAND: "command",
        States.CONTINUE: "continue",
        States.RESULT: "result",
    }

    PROGRESSIONS = {
        States.START: {
            States.DESCRIPTION: _Tokeniser.is_description,
            States.COMMAND: _Tokeniser.is_command,
        },
        States.DESCRIPTION: {
            States.DESCRIPTION: _Tokeniser.is_description,
            States.COMMAND: _Tokeniser.is_command,
        },
        States.COMMAND: {
            States.CONTINUE: _Tokeniser.is_continue,
            States.RESULT: _Tokeniser.is_result,
            States.START: lambda line: _Tokeniser.is_description(line)
            or _Tokeniser.is_command(line),
        },
        States.CONTINUE: {
            States.CONTINUE: _Tokeniser.is_continue,
            States.RESULT: _Tokeniser.is_result,
            States.START: lambda line: _Tokeniser.is_description(line)
            or _Tokeniser.is_command(line),
        },
        States.RESULT: {
            States.RESULT: _Tokeniser.is_result,
            States.START: lambda line: _Tokeniser.is_description(line)
            or _Tokeniser.is_command(line),
        },
    }

    @classmethod
    def progress(cls, from_state, line):
        for to_state, condition in cls.PROGRESSIONS[from_state].items():
            if condition(line):
                return to_state
        return None

    @classmethod
    def state_name(cls, state):
        return cls.STATE_NAMES[state]

    @classmethod
    def get_named_progressions(cls, state):
        progression_states = list(cls.PROGRESSIONS[state].keys())

        # "Start" is just an internal state, so avoid presenting it
        if cls.States.START in progression_states:
            del progression_states[progression_states.index(cls.States.START)]
            progression_states += cls.PROGRESSIONS[cls.States.START].keys()
        return [cls.state_name(s) for s in progression_states]


class Parser(object):
    CONTENT_GETTER = {
        _FSM.States.DESCRIPTION: _Tokeniser.get_description,
        _FSM.States.COMMAND: _Tokeniser.get_command,
        _FSM.States.CONTINUE: _Tokeniser.get_continue,
        _FSM.States.RESULT: _Tokeniser.get_result,
    }

    @classmethod
    def _new_test(cls):
        return dict((key, []) for key in cls.CONTENT_GETTER)

    @staticmethod
    def test_to_test_object(raw_test):
        command = " ".join(
            raw_test[_FSM.States.COMMAND] + raw_test[_FSM.States.CONTINUE]
        )
        description = " ".join(raw_test[_FSM.States.DESCRIPTION])
        result_lines = raw_test[_FSM.States.RESULT]
        return test.Test(command, description=description, result_lines=result_lines)

    @classmethod
    def parse(cls, lines):
        prev_state = _FSM.States.START
        tests = []
        test = cls._new_test()

        for i, line in enumerate(lines):
            if _Tokeniser.is_comment(line) or _Tokeniser.is_empty(line):
                continue

            state = _FSM.progress(prev_state, line)
            if state == _FSM.States.START:
                tests.append(cls.test_to_test_object(test))
                test = cls._new_test()
                state = _FSM.progress(state, line)

            if state is None:
                raise ProgressionError(i, line, prev_state)
            # Preserve newlines for results
            if not state == _FSM.States.RESULT:
                line = line.rstrip()

            test[state].append(cls.CONTENT_GETTER[state](line))
            prev_state = state

        tests.append(cls.test_to_test_object(test))
        return tests


class ProgressionError(exception.CramerError):
    def __init__(self, line_num, line_content, from_state):
        expected_states = _FSM.PROGRESSIONS[from_state].keys()

        message = "Failed to parse line {}: {}\nExpected line of type: {}".format(
            line_num,
            line_content.rstrip(),
            " or ".join(_FSM.get_named_progressions(from_state)),
        )
        super().__init__(message)

        self.line_num = line_num
        self.from_state = from_state
        self.expected_states = [_FSM.state_name(s) for s in expected_states]
