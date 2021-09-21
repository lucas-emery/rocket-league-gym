import rlgym
import traceback
from tests.utils.state_obs import StateObs
from tests.utils.setter_wrapper import SetterWrapper
from tests.cases.boost_pad_test import BoostPadTest

test_suite = [
    BoostPadTest(),
]

# Split tests by config
tests_by_config = {}

for test in test_suite:
    config = frozenset(test.get_config().items())
    tests = tests_by_config.get(config, [])
    tests.append(test)
    tests_by_config[config] = tests

setter_wrapper = SetterWrapper()
total_passed = 0
for config, tests in tests_by_config.items():
    print('Starting RLGym with config:', dict(config))
    # Load env with required config
    env = rlgym.make(obs_builder=StateObs(), state_setter=setter_wrapper, use_injector=True, **dict(config))

    print('--------- Test Set ----------')
    passed = 0
    for test in tests:
        print('\nRunning', type(test).__name__)

        setter_wrapper.set(test.get_state_setter())
        env.reset()
        try:
            test.run(env)
            print('Passed')
            passed += 1
            total_passed += 1
        except Exception:
            print('Failed')
            print(traceback.format_exc())

    print('\n-- Test Set {} - {}/{} --'.format('Passed' if len(tests) == passed else 'Failed', passed, len(tests)))
    env.close()

print('\n-- TEST SUITE {} - {}/{} --'.format('PASSED' if len(test_suite) == total_passed else 'FAILED', total_passed, len(test_suite)))
