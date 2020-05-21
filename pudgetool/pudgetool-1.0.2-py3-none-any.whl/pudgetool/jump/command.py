import click
@click.group(chain=True, invoke_without_command=True)
@click.option('--destination', '-d', default=1)
def jump(destination):
    click.echo('jump to press 1 jms-hz.rokid-inc.com\r\n\tpress 2 to jumpserver.rokid-inc.com')
    import os
    if destination == 1:
        os.system('ssh hui.zhou@jms-hz.rokid-inc.com -p2222')
    elif destination == 2:
        os.system('ssh hui.zhou@jumpserver.rokid-inc.com -p2222')
