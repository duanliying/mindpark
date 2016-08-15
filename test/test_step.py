import pytest
from vizbot.core import Sequential
import vizbot.step
from test.mocks import DurationEnv, Random


STEPS = [
    'Identity', 'Maximum', 'Delta', 'Grayscale', 'Subsample', 'Skip',
    'History', 'Normalize', 'NormalizeReward', 'EpsilonGreedy']


@pytest.fixture(params=STEPS)
def step(request):
    return getattr(vizbot.step, request.param)


@pytest.fixture(params=(1, 2, 17))
def env(request):
    return DurationEnv(request.param)


@pytest.fixture
def interface(env):
    return env.interface


@pytest.fixture
def policy(interface, step):
    policy = Sequential(interface)
    policy.add(step)
    policy.add(Random)
    return policy


class TestStep:

    def test_spaces(self, env, policy):
        # This tests the action and observation spaces since the mock env and
        # the mock monitored random policy check them.
        observation = env.reset()
        policy.begin_episode(True)
        while observation is not None:
            action = policy.step(observation)
            reward, successor = env.step(action)
            policy.experience(observation, action, reward, successor)
            observation = successor
        policy.end_episode()