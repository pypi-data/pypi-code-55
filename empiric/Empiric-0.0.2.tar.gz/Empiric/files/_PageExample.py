from Empiric import Page

########################################################################
##
##  This template can be used to create new pages, which can be used in
##  combination with Empiric.
##
##  To use this template, perform the following steps:
##
##  (1) Rename the files to "pages/Page???.py" and
##      "templates/page???.html", where "???" is some string that
##      serves as a key to recognize the page.
##  (2) Rename all occurances of "pageExample" and "PageExample" in the
##      this file accordingly, while paying attention to capitalization.
##  (3) In the file where your manuscript is defined, add the following
##      import:
##      > from pages.Page??? import page???
##  (4) Now, you can use your new page in the manuscript by adding
##      > page???(m)
##  (5) Congrats, you made it!  Your first page works.
##  (6) You can start tailoring the page to your needs.  To do so,
##      modify the Python and the HTML file accordingly.
##  (7) If your page needs some JavaScript library that has not yet been
##      loaded automatically, you have to add this to the package.json,
##      which you find in your working directy.  Therafter, install the
##      JavaScript library using Yarn in your working directy:
##      > yarn install
##      Then, you can load the library accordingly by inserting
##      corresponding statements in the header block of the file
##      templates/page???.html:
##      > {% block pageHeader %}
##      >   <link rel="stylesheet" href="{{url_for('static', filename='libs/path/to/file.css')}}"/>
##      >   <script src="{{url_for('static', filename='libs/path/to/file.js')}}"></script>
##      > {% endblock %}
##
########################################################################

class PageExample(Page):
  pass

def pageExample(m, title='Example Page', message='Congrats, your page is working!', **kwargs):
  return PageExample(m, 'pageExample.html').run(title=title, message=message, **kwargs)
