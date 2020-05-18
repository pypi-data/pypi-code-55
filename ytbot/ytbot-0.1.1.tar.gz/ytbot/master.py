import asyncio
import click

from .cfg import configure 
from .puppet import run 
from .cfg import reset

# Pass configurations with this dictionary
SETTINGS = dict()



@click.command()
@click.argument('step',default = '')
@click.option('--headless','-h', default=False, is_flag = True)
def main( step, headless):

    SETTINGS['headless'] = headless
    


    if step == 'run':
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run(SETTINGS))
            
        except Exception as e:
            help_text = '''
Hey There! Did face any issue while running the app?
Let me Know and I'll try to fix it.
for any additional information, contact me at: 'muhammadfahim010@gmail.com'
Also any kind of feedback would be super encouraging.
Peace Out '''
            print(help_text)
            raise SystemExit('Exit from Bot!')
    
    elif step == 'configure':
        configure(SETTINGS)

    elif step == 'reset':
        reset()

    else:
        print(
        '''Usage: 
            ytbot    [OPTIONS] [OPTIONS]

            ytbot    configure                    configure bot for 
                                                  first time

            ytbot    run                          after configuration
                                                  run the bot
            
            ytbot    reset                        reset the configuration
                                                  and start anew

            ytbot    run [--headless][-h]         To run in headless mode!
                                                  Default is headful!!!

''')

        




if __name__=='__main__':
    main()
