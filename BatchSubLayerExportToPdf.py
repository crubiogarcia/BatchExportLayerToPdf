! _-RunPythonScript (
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import System
from System.Windows.Forms import FolderBrowserDialog, DialogResult

dpi = 300

# Prompt the user to input a Sring
def get_literal_string(prompt):
    gs = Rhino.Input.Custom.GetString()
    gs.SetCommandPrompt(prompt)
    result = gs.GetLiteralString()
    if (result == Rhino.Input.GetResult.String):
        return gs.StringResult().Trim()
    return None
# Function to get a page view by its name
def get_page_view_by_name(page_name):
    # Retrieve all page views
    pages = sc.doc.Views.GetPageViews()
    # Iterate through the pages
    for page in pages:
        # Check if the page name matches the desired name
        if page.PageName == page_name:
            return page
        # Raise an exception if no page is found with the specified name
    raise Exception("Error: No existing page found with that name")
# Get folder path
def ask_for_folder_path():
    dialog = FolderBrowserDialog()
    dialog.Description = "Select a folder"
    dialog.ShowNewFolderButton = True  # Allow the user to create a new folder if needed

    result = dialog.ShowDialog()
    
    if result == DialogResult.OK:
        folder_path = dialog.SelectedPath
        return folder_path
    else:
        raise Exception("Error: No folder selected")

#Get Layer
mainlayername = rs.GetLayer("Select Layer")
parentLayer = Rhino.RhinoDoc.ActiveDoc.Layers.FindName(mainlayername)

#Get the name of the page
getpage = get_literal_string("Enter the Page Name")
#Access the page name
try:
    pag = get_page_view_by_name(getpage)
except Exception as e:
    print(e)
    raise  # Reraise the exception to halt script execution

#Get folder path
try:
    folder_path = ask_for_folder_path()
except Exception as e:
    print(e)
    raise  # Reraise the exception to halt script execution

folder_path = folder_path + "\\"

folder_path = folder_path + "\\"


#turn off all sublayers and remember initial visibility state
initialstate = []
for subLayer in parentLayer.GetChildren():
    initialstate.append(rs.LayerVisible(subLayer.Name))
    rs.LayerVisible(subLayer.Name, False)

#print every sublayer   
for subLayer in parentLayer.GetChildren():
    #turn layer on
    rs.LayerVisible(subLayer.Name, True)
    #printing
    pdf = Rhino.FileIO.FilePdf.Create()
    
    capture = Rhino.Display.ViewCaptureSettings(pag, dpi)
    pdf.AddPage(capture)

    fnameall = folder_path + subLayer.Name + '.pdf'
    print(fnameall)
    pdf.Write(fnameall)
    
    #turn sublayer off
    rs.LayerVisible(subLayer.Name, False)

#Return Visibility to initial state
for i in range(len(parentLayer.GetChildren())):
    rs.LayerVisible(parentLayer.GetChildren()[i].Name, initialstate[i])
    

print("Batch Print Done")

)

Carmen Rubio Garcia
Architect ARB

Foster + Partners
Riverside, 22 Hester Road 
London SW11 4AN
crubiogarcia@fosterandpartners.com
www.fosterandpartners.com

