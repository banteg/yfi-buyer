import pytest
from ape import convert
from ape_tokens import tokens


@pytest.fixture
def milky(accounts):
    return accounts[0]


@pytest.fixture
def bunny(accounts):
    return accounts[1]


@pytest.fixture
def rune(accounts):
    return accounts[2]


@pytest.fixture
def buyer(project, milky):
    return project.YfiBuyer.deploy(sender=milky)


@pytest.fixture
def brk_a():
    return convert("465_000 DAI", int)


@pytest.fixture
def waifu():
    return convert("1 YFI", int)


@pytest.fixture
def yfi(project, bunny, accounts, waifu):
    token = project.ERC20.at(tokens["YFI"].address)
    whale = "0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52"
    token.transfer(bunny, waifu, sender=accounts[whale])
    return token


@pytest.fixture
def dai(project, rune, accounts, brk_a):
    token = project.ERC20.at(tokens["DAI"].address)
    whale = "0x075e72a5eDf65F0A5f44699c7654C1a76941Ddc8"
    token.transfer(rune, brk_a, sender=accounts[whale])
    return token
