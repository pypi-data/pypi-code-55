from Empiric.Pages.Page import Page

class PageAccessCode(Page):
  pass

def pageAccessCode(m, showErrorMessage=False, **kwargs):
  return PageAccessCode(m, 'pageAccessCode.html').render(hideStatisticsByDefault=True, showErrorMessage=showErrorMessage, **kwargs)
