import ape


def test_buyback_with_dai(buyer, yfi, dai, bunny, milky, treasury):
    buyer.set_treasury(treasury, sender=milky)
    dai.transfer(buyer, "100_000 DAI", sender=milky)
    yfi_amount = ape.convert("1 YFI", int)
    yfi.approve(buyer, yfi_amount, sender=bunny)
    receipt = buyer.buy_dai(yfi_amount, sender=bunny)
    log = next(buyer.Buyback.from_receipt(receipt))
    print(log.event_arguments)
    print(log.dai / log.yfi, "YFI/DAI")

    assert log.buyer == bunny
    assert log.yfi == yfi_amount
    assert yfi.balanceOf(treasury) == yfi_amount
    assert dai.balanceOf(bunny) == log.dai


def test_buyback_stale_oracle(buyer, yfi, dai, bunny, milky, chain):
    dai.transfer(buyer, "100_000 DAI", sender=milky)
    yfi.approve(buyer, yfi.balanceOf(bunny), sender=bunny)

    chain.pending_timestamp += 86400

    with ape.reverts():
        buyer.buy_dai("1 YFI", sender=bunny)


def test_price(buyer):
    price = buyer.price()
    assert price > 0


def test_set_admin(buyer, milky, bunny):
    assert buyer.admin() == milky

    with ape.reverts():
        buyer.set_admin(bunny, sender=bunny)

    buyer.set_admin(bunny, sender=milky)
    assert buyer.admin() == bunny


def test_sweep(buyer, yfi, dai, bunny, milky):
    yfi.transfer(buyer, 100, sender=bunny)
    dai.transfer(buyer, 100, sender=milky)

    with ape.reverts():
        buyer.sweep(yfi, sender=bunny)

    buyer.sweep(yfi, sender=milky)
    assert yfi.balanceOf(milky) == 100

    before = dai.balanceOf(milky)
    buyer.sweep(dai, 50, sender=milky)
    assert dai.balanceOf(milky) == before + 50


def test_set_treasury(buyer, bunny, milky, treasury):
    assert buyer.treasury() == treasury

    with ape.reverts():
        buyer.set_treasury(bunny, sender=bunny)

    buyer.set_treasury(milky, sender=milky)
    assert buyer.treasury() == milky


def test_buyback_with_stream(buyer, bunny, dai, yfi, chain, treasury, stream):
    yfi.approve(buyer, yfi.balanceOf(bunny), sender=bunny)

    # we can't skip too far because of the oracle staleness check
    chain.pending_timestamp = chain.pending_timestamp + 600
    receipt = buyer.buy_dai("1 gwei", sender=bunny)

    log = next(buyer.Buyback.from_receipt(receipt))
    print(log.event_arguments)
    print(log.dai / log.yfi, "YFI/DAI")

    assert log.buyer == bunny
    assert log.yfi == yfi.balanceOf(treasury)
    assert log.dai == dai.balanceOf(bunny)
