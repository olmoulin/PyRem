# PyRem

This tools allow to syncrhonize file and browse the directory structure of the remarkable 2 device on linux.
I created this quick tool in order to be able to browse my remarkable on Asahi Linux ... but I think everybody has the same problem with all linux as remarkable is not offering a client for this platform ... (which is quite strange, knowing that the remarkable itself runs under linux ...)
<br>
So this is a quick python script which can be of help (comes with no warranty, GNU license.)

Please note that the system (interactive mode as well as command line) replaces all the blank in the filenames by the '_' character, so if you want to access the 'Quick Note' file under the root folder of the remarkable, it has to be refered to as /Quick_Note. 

# Install
<br>Clone the git repository
> git clone https://gitlab.com/open_source_omn/PyRem.git

<br>Install sshpass, rsync, python (built on 3.8)
<br>Fedora : 
> sudo dnf install sshpass rsync

<br>Debian : 
> sudo apt-get install sshpass rsync

<br>Under your Python environment:
> pip install numpy

<br>Then you are good to go.

# Interactive usage
In the PyRem directory, launch:
> python pyrem.py

or 

> python pyrem.py cli

<br>List the interactive commands:
> help

<br>Set your remarkable password:
> passwd

<br>The system will ask you to provide the password of your remarkable.
<br>You can find it in Menu/Settings/Help/Copyright and Licenses/General Information on your Remarkable

<br>Synchronize your remarkable (after setting the password of course and connecting the remarkable to USB):
> sync

<br>It can take some time, the system retrive the metadata as well as all pdfs from the remarkable

<br>Display files and folders tree:
> tree

<br>List current directory:
> ls

<br>It shows the [subdirectories] and files in the current remarkable folder

<br>Move in subdirectory:
> cd [subdirectory]

<br>Do not put the bracket, they are only displayed to show difference between directories and files

<br>Move up to parent directory:
>  cd ..

<br>Export PDF: (and also remarkable files in the future):
> export [filename] [local directory]

<br>For example export My_great_pdf.pdf ~/
<br>This will create a copy of the PDF in the local folder

# Command line usage

<br>List the command line options:
> help

<br>Set your remarkable password:
> python pyrem.py passwd [password]

<br>The system will ask you to provide the password of your remarkable.
<br>You can find it in Menu/Settings/Help/Copyright and Licenses/General Information on your Remarkable

<br>Synchronize your remarkable (after setting the password of course and connecting the remarkable to USB):
> python pyrem.py sync

<br>It can take some time, the system retrive the metadata as well as all pdfs from the remarkable

<br>Display all files and folders tree
> python pyrem.py tree

<br>Export PDF: (and also remarkable files in the future):
> python pyrem.py export [path to remarkable file] [local directory]

<br>For example: export /Folder1/Folder2/My_great_pdf.pdf ~/
<br>This will create a copy of the PDF in the local folder

<br>Import PDF: Still experimental but works! - import file under the remarkable root folder
> python pyrem.py import [local path to the PDF]

<br>For example: import ~/My_great_pdf.pdf 
<br>Please note that after the import the remarkable will restart its UI, it is needed in order to refresh the remarkable internal cache and indexing the new imported file.

# Development progress
<br>That's all for now ... (in fact it was just a couple of hours coding, so expect a little bit more soon ...)

