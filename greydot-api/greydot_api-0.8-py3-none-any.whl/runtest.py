import tests


def run():
    print("Testing airtime...")
    tests.test_airtime()
    print("Testing b2c...")
    tests.test_b2c()
    print("Testing wallet...")
    tests.test_wallet()
    print("Testing signup...")
    tests.test_signup()
    print("Testing sms...")
    tests.test_sms()
    print("DONE")


if __name__ == "__main__":
    run()
