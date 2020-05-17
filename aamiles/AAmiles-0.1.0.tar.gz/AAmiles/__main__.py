from AAmiles import app

if __name__ == '__main__':
    val = 'S'
    while val == 'S' or val == 's':
        try:
            val = app.run()
        except:
            print('Intentar nuevamente?')
            val = input('(S/N) :')