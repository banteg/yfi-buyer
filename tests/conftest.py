from contextlib import contextmanager

import pytest
from ape_tokens import tokens
from eth_utils import encode_hex


@pytest.fixture(scope='session')
def impersonate_contract(chain):
    """
    Allows to impersonate a contract on Anvil and bypass "EVM error RejectCallerWithCode".
    """
    make_request = chain.provider.web3.manager.request_blocking

    @contextmanager
    def wrapper(address):
        code = encode_hex(chain.provider.get_code(address))
        make_request("anvil_setCode", [address, ""])
        yield
        make_request("anvil_setCode", [address, code])

    return wrapper


@pytest.fixture(scope='session')
def milky(accounts):
    return accounts[0]


@pytest.fixture(scope='session')
def bunny(accounts):
    return accounts[1]


@pytest.fixture(scope='session')
def treasury(accounts):
    return accounts[2]


@pytest.fixture(scope='session')
def buyer(project, milky, treasury):
    """
    YfiBuyer(admin=milky, treasury=treasury, rate=0)
    """
    contract = project.YfiBuyer.deploy(sender=milky)
    contract.set_treasury(treasury, sender=milky)
    return contract


@pytest.fixture(scope='session')
def yfi(project, bunny, accounts, impersonate_contract):
    """
    YFI token with balanceOf(bunny) = 10 YFI
    """
    token = project.ERC20.at(tokens["YFI"].address)
    whale = "0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52"
    with impersonate_contract(whale):
        token.transfer(bunny, "10 YFI", sender=accounts[whale])
    return token


@pytest.fixture(scope='session')
def dai(project, milky, accounts):
    """
    DAI token with balanceOf(milky) = 1m DAI
    """
    token = project.ERC20.at(tokens["DAI"].address)
    whale = "0x075e72a5eDf65F0A5f44699c7654C1a76941Ddc8"
    token.transfer(milky, "1_000_000 DAI", sender=accounts[whale])
    return token


@pytest.fixture(scope='session')
def llamapay(chain):
    contract = chain.contracts.instance_at("0x60c7B0c5B3a4Dc8C690b074727a17fF7aA287Ff2")
    return contract
