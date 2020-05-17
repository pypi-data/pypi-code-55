def test_install():
    try:
        import ppong
        print(f">>> TEST SUCCESSFUL")
    except:
        print(f">>> TEST NOT SUCCESSFUL. Most probabaly missing dependencies.")

test_install()