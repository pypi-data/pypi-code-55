"""
This code produces the NPK documentation from the ProcessXX python files

File are such as:

triple quote
    Mains doc
triple quote

def one_entry:
    triple quote
        doc of the entry
    triple quote
    ....code...
    # %action% name details
    # parameters
    # ....
    ....code...
    # %action% name details
    # parameters
    # ....
def another entry:

etc...

"""
import re
import time

def build_doc(file):
    """builds the documentation for the NPK ProcessXX files
    """

    # open files
    fin=open(file,'r')
    fileout=re.sub("\.py",".html",file)
    print fileout
    fout=open("Doc/"+fileout,'w')
# read-in python file
    f=fin.read()
    lines = f.split("\n")
# write doc file
    header(fout,file)
#first leading comments
    copy_pre(fout,lines)

    if file != 'Interface.py':
        #then process each entries
        process_entries(fout,lines)

    fout.writelines('</table></body></html>\n')
    fout.close()

def static_pages():
	"""builds the static documentation pages npk.html and introduction.html"""
	print "index.html"
	npk_html()
	print "introduction.html"
	intro_html()

def intro_html():
	"called by static_pages()"
	f=open("Doc/introduction.html",'w')
	f.writelines("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
  <title>introduction to NPK</title>
  <meta content="Marc A Delsuc" name="author">
</head>
<body>
<table style="text-align: left; margin-left: auto; margin-right: auto;" summary="heading" border="0" cellpadding="2" cellspacing="0" width="100%">
  <tbody>
    <tr bgcolor="#7799ee">
      <td align="center" valign="bottom">&nbsp;<br>
      <font color="#ffffff" face="helvetica, arial">&nbsp;<br>
      <big><big><strong><big> NPK<br>
      </big><span style="font-style: italic;">-Documentation -</span></strong></big></big></font></td>
    </tr>
  </tbody>
</table>
<p style="text-align: right;"><span style="font-style: italic;">an NMR processing program</span>.</p>
<p style="text-align: center;"><big>NPK stands for <strong>N</strong>MR<strong>P</strong>rocessing<strong> K</strong>ernel.</big></p>
<p>NPK implements</p>
<ul>
  <li>standard processing for 1D 2D and 3D experiments (3D is not available in level 1 yet)</li>
  <li>automatic processing of standard NMR experiments, based on carefully chosen defaut processing parameters</li>
  <li>MaxEnt processing for spectral analysis, with support for partial sampling</li>
  <li>Processing a DOSY experiments, with a MaxEnt implementation of the Inverse Laplace Transform</li>
  <li>a python 2.1 environment for easy NMR processing programming</li>
</ul>
<p>NPK does <em>not</em> implement&nbsp;</p>
<ul>
  <li>an interactive NMR program for displaying the spectra</li>
  <li>any user graphic interface</li>
</ul>
<p>NPK shares the same binary&nbsp;file formats with <a style="font-style: italic;" href="http://www.cbs.cnrs.fr/GIFA/">Gifa.</a> As such, it can easily share data with <span style="font-style: italic;">Gifa</span> compatible programs.<br>
For instance <span style="font-style: italic;">Gifa</span> 4 or <span style="font-style: italic;">Gifa</span> 5 can be used to display NPK results, or can even be programmed to launch NPK scripts.<br> NMRNoteBook is a commercial program which present a very easy to use graphic interface, and can import and export <span style="font-style: italic;">Gifa</span> files.</p>
<br>
as a first contact, NPK can be seen as composed of several modules:
<ol>
  <li>a <span style="font-weight: bold;">modeling</span> of the NMR processing, which permits to very simply describe an experiment and the processing to apply on it, &nbsp;along with simple commands to realize this processing.<br>
This level permits to simply start a processing or interact interactively with the data.</li>
  <li>a set of <span style="font-weight: bold;">high level commands</span>, implementing the high level operation needed for NMR (such as shearing or automatic phasing for instance)<br>
This level permits to rapidely implement new processing&nbsp;strategies.</li>
  <li>a set of <span style="font-weight: bold;">low level commands</span>, called the Kernel, tuned for efficient NMR
processing.<br>
This comprises the buffers for 1D, 2D and 3D processing, is composed by a set of fundamental&nbsp; mathematical operation.</li>
</ol>
<br>
<p>Because of these three levels of organisation, the documentation itself is organized in three levels.</p>
<ol>
  <li>The modeling level :<br>
Is typically called from the command line, using the Launch method. The modeling implement actions which require parameters.</li>
  <ul>
    <li><a href="Launch.html">Launch</a> presents the main user interface</li>
    <li><a href="Process1D.html">Process1D</a> presents all the parameters for processing 1D experiments</li>
    <li><a href="Process2D.html">Process2D</a> presents all the parameters for processing 2D experiments</li>
    <li><a href="Process3D.html">Process3D</a> presents all the parameters for processing 3D experiments</li>
    <li><a href="ProcessDosy.html">ProcessDosy</a> presents all the parameters for processing DOSY experiments</li>
  </ul>
  <li>The high level processing library :<br>
is typically used in python programs which may use the following methods.</li>
  <ul>
    <li><a href="Generic.html">Generic</a> contains most of the needed NMR functions</li>
    <li><a href="GenericDosy.html">GenericDosy</a> contains function specific to DOSY processing</li>
  </ul>
  <li>The low level&nbsp;processing library :<br>
this one implements the processing buffers and the basic mathematical methods to interact with the data-set. It is implemented as a jni binary library.</li>
  <ul>
    <li><a href="kernel/thedoc.html">presented here</a><br>
Note that this documentation is still incomplete and in beta state.</li>
  </ul>
</ol>
<p>NPK is developped as a plateform independent program, and
relies on computer several langages.</p>
<p>NPK architecture can be presented as follow :</p>
<p></p>
<table style="text-align: left; width: 719px; height: 140px; margin-left: 40px;" border="2">
  <tbody>
    <tr>
      <td>
      <table style="text-align: left; width: 719px; height: 140px;" border="0" cellpadding="2" cellspacing="4">
        <tbody>
          <tr>
            <td style="width: 197px;"></td>
            <td style="width: 293px; background-color: rgb(119, 153, 238);"><span style="font-style: italic;">usage</span></td>
            <td style="width: 201px; background-color: rgb(119, 153, 238);"><span style="font-style: italic;">computer language</span></td>
          </tr>
          <tr>
            <td style="width: 197px; background-color: rgb(255, 204, 102);">command line processing<br>Processing Modeling</td>
            <td style="width: 293px;">launch batch or interactive processing from the command line. </td>
            <td style="width: 201px;">parameter files<br>
            </td>
          </tr>
          <tr>
            <td style="width: 197px; background-color: rgb(255, 204, 102);">high level library</td>
            <td style="width: 293px;">python scripts for special processing</td>
            <td style="width: 201px;">python</td>
          </tr>
          <tr>
            <td style="width: 197px; background-color: rgb(255, 204, 102);">&nbsp;low level library -&nbsp;wrapper</td>
            <td style="width: 293px;">called directly from python script, mixed with high-level methods.</td>
            <td style="width: 201px;">java</td>
          </tr>
          <tr>
            <td style="width: 197px; background-color: rgb(204, 204, 204);">low level library - binary</td>
            <td style="width: 293px;">not used directly<br>
            </td>
            <td style="width: 201px;">FORTRAN</td>
          </tr>
        </tbody>
      </table>
      </td>
    </tr>
  </tbody>
</table>
<p></p>
<p>If you were familliar with <span style="font-style: italic;">Gifa,</span> the low level
library is built with the same principles. Most <span style="font-style: italic;">Gifa</span> processing
commands are implemented in the NPK low level library.&nbsp;<br>
So:</p>
<ul>
  <li>if XYZ is a kernel command in <span style="font-style: italic;">Gifa,&nbsp;</span>
com_xyz() is a low level method in NPK; usually xyz() is also available;</li>
  <li>if $ABC is a kernel context in <span style="font-style: italic;">Gifa</span>,
&nbsp;then get_abc() is the value in NPK;</li>
  <li>if $ABC[i] is a kernel context in <span style="font-style: italic;">Gifa</span>,&nbsp;
then geta_abc(i) is the value in NPK;</li>
  <li><strong>writec</strong>(filename) and <strong>read</strong>(filename) are the low-level method to write/read
NMR file in the <span style="font-style: italic;">Gifa</span>
format;</li>
</ul>
<p>If you are familliar with python, then note that it is the
Java implementation&nbsp;jython 2.1 which is used. You will find
the full details on jython <a href="http://www.jython.org/Project/index.html">here</a>.
It implements python 2.1. You can find the difference between the
different version of python <a href="http://rgruet.free.fr/">here</a>.</p>
<p><i>NPK is an NMR processing program developped by Marc A. Delsuc Vincent Catherinot, Dominique Tramesel, and others.</i></p>
</body>
</html>
	""")

def npk_html():
	"called by static_pages()"
	f=open("Doc/index.html",'w')
	f.writelines("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
  <title>NPK</title>
  <meta content="Marc A Delsuc" name="author">
</head>
<body>
<table style="text-align: left; margin-left: auto; margin-right: auto;" summary="heading" border="0" cellpadding="2" cellspacing="0" width="100%">
  <tbody>
    <tr bgcolor="#7799ee">
      <td align="center" valign="bottom">&nbsp;<br>
      <font color="#ffffff" face="helvetica, arial">&nbsp;<br>
      <big><big><strong><big> NPK<br>
      </big><span style="font-style: italic;">-
Documentation -</span></strong></big></big></font></td>
    </tr>
  </tbody>
</table>
<p style="text-align: right;"><span style="font-style: italic;">an NMR processing program</span>.</p>
<p style="text-align: center;"><big>NPK stands for <strong>N</strong>MR
<strong>P</strong>rocessing<strong> K</strong>ernel.</big></p>
<h2>What is NPK</h2>
<ul>
  <li><a href="introduction.html">Introduction</a></li>
</ul>
<h2>Complete documentation</h2>
<ol>
  <li>The modeling level :
  </li>
  <ul>
    <li><a style="font-weight: bold;" href="Launch.html">Launch</a><br>&nbsp;the main user interface</li>
    <li><a style="font-weight: bold;" href="Process1D.html">Process1D</a><br>&nbsp;all the parameters for processing 1D experiments</li>
    <li><a style="font-weight: bold;" href="Process2D.html">Process2D</a><br>&nbsp;all the parameters for processing 2D experiments</li>
    <li><a style="font-weight: bold;" href="Process3D.html">Process3D</a><br>&nbsp;all the parameters for processing 3D experiments</li>
    <li><a style="font-weight: bold;" href="ProcessDosy.html">ProcessDosy</a><br>&nbsp;all the parameters for processing DOSY experiments</li>
  </ul>
  <li>The high level processing library :<br>  </li>
  <ul>
    <li><a style="font-weight: bold;" href="Generic.html">Generic</a><br>&nbsp;most of the needed NMR functions</li>
    <li><a style="font-weight: bold;" href="GenericDosy.html">GenericDosy</a><br>contains function specific to DOSY processing</li>
  </ul>
  <li>The low level&nbsp;processing library :<br>  </li>
  <ul>
    <li><a style="font-weight: bold;" href="kernel/thedoc.html">presented here</a> <br>
Note that this documentation is still incomplete and in beta state.</li>
  </ul>
</ol>
<p><i>NPK is an NMR processing program developped by Marc A. Delsuc Vincent Catherinot, Dominique Tramesel, and others.</i></p>
</body>
</html>
	""")
	f.close()

def header(fout,file):
    # writes html header
    fout.writelines(
    """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
    <html>
    <head>
    <META http-equiv="Content-Type" Content="text/html; charset=ISO-8859-1">
    """)
    title = "NPK: "+ file
    fout.writelines( '<TITLE>' + title + '</TITLE>\n</head>\n<body>\n' )
    fout.writelines( """
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#7799ee">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong>
        """+title+"""
</strong></big></big>"""+time.asctime()+"""</font></td></tr></table>
        """)


def copy_pre(fout,lines):
    """ Process a comment block separated by the triple quote
    """
    l=lines.pop(0)
    while (not re.search('"""',l)):
        l=lines.pop(0)
    l=lines.pop(0)
    block=[]
    while (not re.search('"""',l)):
        l=re.sub(r'%author%\s*(.*)', r'<strong>Author:</strong> &nbsp;&nbsp;\1', l)
        l=re.sub(r'%version%\s*(.*)', r'<strong>Version:</strong> &nbsp;&nbsp;\1', l)
        l=re.sub(r'%dimensionality%\s*(.*)', r'<strong>Dimensionality:</strong> &nbsp;&nbsp;\1', l)
        l=re.sub(r'%F([123])-input-domain%\s*(.*)', r'<strong>Input Domain in F\1:</strong> &nbsp;&nbsp;\2', l)
        l=re.sub(r'%F([123])-output-domain%\s*(.*)', r'<strong>Output Domain in F\1:</strong> &nbsp;&nbsp;\2', l)
        
        block.append(l+"\n")
        l=lines.pop(0)
    fout.writelines('<pre>\n')
    fout.writelines(block)
    fout.writelines('</pre>\n')

def process_entries(fout,lines):
    """ Process all entry definitions
    """
    while lines:
        l=lines.pop(0)
        func = re.findall('^def\s*(\w*)\((.*)\):',l)     # check if new entry found
        if func:     # if new entry found
            (title,arg)=func[0]
            fout.writelines("""
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="entries">
<tr bgcolor="#eeaa77">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>"""+title+"""</strong>("""+arg+""")</big></font></td></tr>
<tr><td bgcolor="#eeaa77"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%">
        """)
            copy_pre(fout,lines)   # copy first block

            # get entry
            entry=[]
            while lines:
                l=lines.pop(0)
                if re.match('^def (\w*)',l):
                    lines.insert(0,l)
                    break
                else:
                    entry.append(l)
            text=process_entry(entry)
            if text != "":
                fout.writelines('<big><font color="#0000CC" face="helvetica, arial"><strong>Actions</strong></font></big><hr>')
                fout.writelines(text)
            fout.writelines("</td></tr></table><p></p>")

def process_entry(entry):
    """ process one entry
    """
    # get each action
    fout = ""
    while entry:
        l=entry.pop(0)
        t = re.findall('^\s*#\s*%action%\s*(.*)$',l)  # search action
        if t:
            action=t[0]
            param=[]
            while entry:
                l=entry.pop(0)
                s = re.findall('^\s*#\s*(.*)$',l)  # get text
                if s:
                    param.append(s[0])
                else:
                    break
            fout = fout +  "<ul>"
            fout = fout + process_action(action,param)
            fout = fout +  ("</ul>")
    if fout != "":
        return "<dl>" + fout +  "</dl>\n"
    else:
        return ""

def process_action(action,param):
    fout ='<p></p><dl><dt><font color="#0000CC" face="helvetica, arial"><strong>'+action+'</strong></font></dt><dd>'
    while param:
        l=param.pop(0)
        l=re.sub(r'%param%\s*(\w*)\s*(.*)', r'<br><li><strong>\1:</strong> &nbsp;&nbsp;\2</li>', l)
        l=re.sub(r'%param_cond%\s*(.*)', r'<br><li><strong><i>conditions:</i></strong> &nbsp;&nbsp;\1</li>', l)
        l=re.sub(r'%return%\s*(.*)', r'<br><li><strong><i>returned value:</i></strong> &nbsp;&nbsp;\1</li>', l)
        l=re.sub(r'%param_exclusive%\s*(.*)', r'<br><li><strong><i>exclusive parameters:</i></strong> &nbsp;&nbsp;\1</li>', l)
        l=re.sub(r'%use%\s*(.*)', r'<br><li><strong><i>input value:</i></strong> &nbsp;&nbsp;\1</li>', l)
        
        fout = fout +  "<tt>"+l+"</tt><br>\n"
    fout = fout +  "</dd></dl>\n"
    return fout


# Now do the work
static_pages()
build_doc("Process1D.py")
build_doc("Process2D.py")
build_doc("Process3D.py")
build_doc("ProcessDosy.py")
build_doc("Launch.py")
    
