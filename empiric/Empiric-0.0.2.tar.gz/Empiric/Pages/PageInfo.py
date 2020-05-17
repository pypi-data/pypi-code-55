from Empiric.Pages.Page import Page

class PageInfo(Page):
  pass

def pageInfo(m, title='', message='', **kwargs):
  return PageInfo(m, 'pageInfo.html').run(hideStatisticsByDefault=True, title=title, message=message, **kwargs)
