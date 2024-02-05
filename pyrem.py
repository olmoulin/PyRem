import os
import sys
import subprocess
import numpy as np


def refresh_file_structure():
    file_structure=[]
    for file in os.listdir('./metadata'): 
        if file.endswith(".metadata"): 
            file_id = ''
            file_parent = ''
            file_name = ''
            file_path = f"./metadata/"+file
            with open(file_path,'r') as fmdata:
                file_id = file[:-9]
                Lines = fmdata.readlines()
                for line in Lines:
                    if "parent" in line:
                        file_parent=line[15:]
                        file_parent=file_parent[:-3]
                    if "visibleName" in line:
                        file_name=line[20:]
                        file_name=file_name[:-2]
                        file_name=file_name.replace(' ','_')
                    if "type" in line:
                        file_type=line[13:]    
                        file_type=file_type[:-3]
                fmdata.close()
            current_file = [file_parent,file_id,file_name,file_type]
            file_structure.append(current_file)
    file_structure=np.array(file_structure)
    return(file_structure)

def display_tree(file_structure,current_dir,indent=0):
    bool_array = file_structure[:,0]==current_dir
    current_folder_files = file_structure[bool_array]
    bool_array_folders = current_folder_files[:,3]=="CollectionType"
    current_folder_files_folder = current_folder_files[bool_array_folders]
    bool_array_files = current_folder_files[:,3]=="DocumentType"
    current_folder_files_files = current_folder_files[bool_array_files]
    for i in range(0,current_folder_files_files.shape[0]):
        str="|"
        for j in range(0,indent):
            str=str+"    |"
        str=str+"-"
        print(str+current_folder_files_files[i][2])
    for i in range (0,current_folder_files_folder.shape[0]):
        str="|"
        for j in range(0,indent):
            str=str+"    |"
        str=str+"-"
        print(str+"["+current_folder_files_folder[i][2]+"]")
        display_tree(file_structure,current_folder_files_folder[i][1],indent+1)





def main():
    command = ""
    current_parent=''
    current_parent_parent =''
    remarkable_password=''
    if os.path.exists('./passwd.rm'):
        with open('./passwd.rm','r') as pfile:
            remarkable_password=pfile.read()
            pfile.close()
    if os.path.exists('./pdf/')==False:
        os.system('mkdir pdf')
    if os.path.exists('./metadata/')==False:
        os.system('mkdir metadata')   
    if os.path.exists('./content/')==False:
        os.system('mkdir content')     
    print("Building file tree from local cache ...")
    print("Please consider running sync to ensure the file structure is actual.")
    file_structure = refresh_file_structure()
    param_start = sys.argv
    main_param_param1 = ""
    main_param_param2 = ""
    main_param = "cli"
    if len(param_start)>1:
        main_param = param_start[1]
    if len(param_start)>2:
        main_param_param1 = param_start[2]
    if len(param_start)>3:
        main_param_param2 = param_start[3]
    has_good_param = False
    if main_param=="cli":
        has_good_param=True
        while command!="quit":
            command = input("Pyrem > ")
            com = command.split()
            if com[0]=="passwd":
                passwd = input("Remarkable password : ")
                remarkable_password=passwd
                with open('./passwd.rm','w') as pfile:
                    pfile.write(remarkable_password)
                    pfile.close()
            if com[0]=="help":
                print("List of commands:")
                print("  sync : synchronize with remarkable tablet")
                print("  ls : list current directory files and folders")
                print("  tree : display all files and folders in a tree format")
                print("  cd <..|folder> : move to parent folder (..) or into folder.")
                print("  export <file> <local folder> : export the file in the current folder to a folder on local machine")                
            if com[0]=="tree":
                print("Remarkable files and folders tree:")
                display_tree(file_structure,'')
            if com[0]=="sync":
                print("Importing metadata from Remarkable ...")
                exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" root@10.11.99.1:~/.local/share/remarkable/xochitl/*.metadata ./metadata/')
                if exit_code!=0:
                    print("Sync failed, check the remarkable is connected to a usb port, switched on and the provided password is the right one.")
                    print("The data displayed in the system may be outdated until the problem is fixed.")
                print("Downloading PDFs from Remarkable ...")
                exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" root@10.11.99.1:~/.local/share/remarkable/xochitl/*.pdf ./pdf/')
                if exit_code!=0:
                    print("Sync failed, check the remarkable is connected to a usb port, switched on and the provided password is the right one.")
                    print("The data displayed in the system may be outdated until the problem is fixed.")
                print("Regenerating local representation of file tree ...")
                file_structure = refresh_file_structure()
            if com[0]=="debug_structure":
                print(file_structure)
                
            if com[0]=="debug_ls":
                bool_array = file_structure[:,0]==current_parent
                current_folder_files = file_structure[bool_array]
                print(current_folder_files)
            if com[0]=="debug_metadata":
                for file in os.listdir('./metadata'): 
                    if file.endswith(".metadata"): 
                        with open(file_path,'r') as fmdata:
                            print(fmdata.read())
                            fmdata.close()
            if com[0]=="ls":
                bool_array = file_structure[:,0]==current_parent
                current_folder_files = file_structure[bool_array]
                bool_array_folders = current_folder_files[:,3]=="CollectionType"
                current_folder_files_folder = current_folder_files[bool_array_folders]
                bool_array_files = current_folder_files[:,3]=="DocumentType"
                current_folder_files_files = current_folder_files[bool_array_files]
                for fld in current_folder_files_folder[:,2]:
                    print("["+fld+"]")
                for fls in current_folder_files_files[:,2]:
                    print(fls)
            if com[0]=="cd":
                if len(com)<2:
                    print("Usage: cd <..|folder>")
                else:
                    if com[1]!="..":
                        bool_array = file_structure[:,0]==current_parent
                        current_folder_files = file_structure[bool_array]
                        bool_target = current_folder_files[:,2]==com[1]
                        target_folder = current_folder_files[bool_target]
                        if target_folder.size==0:
                            print("This folder does not exist or this does not refer to a folder.")
                        else:
                            current_parent_parent=current_parent
                            current_parent=target_folder[0][1]
                    else:
                        if current_parent=='':
                            print("Already at the root of the file structure.")
                        else:
                            current_parent=current_parent_parent
            if com[0]=="export":
                if len(com)<3:
                    print("Usage: export <file> <localfolder>")
                else:
                    bool_array = file_structure[:,0]==current_parent
                    current_folder_files = file_structure[bool_array]
                    bool_target = current_folder_files[:,2]==com[1]
                    target_file = current_folder_files[bool_target]
                    if target_file.size==0:
                        print("The specified file does not exists.")
                    else:           
                        if os.path.exists('./pdf/'+target_file[0][1]+'.pdf') == False:
                            print('Export works only with PDFs ... for now :-) ')
                        else:
                            if com[2].endswith('/'):
                                exit_code=os.system('cp ./pdf/'+target_file[0][1]+'.pdf '+com[2]+target_file[0][2])
                            else:
                                exit_code=os.system('cp ./pdf/'+target_file[0][1]+'.pdf '+com[2]+'/'+target_file[0][2])
                            if exit_code!=0:
                                print("Export failed, please check that output directory exists.")
    if main_param=="tree":
        has_good_param=True
        print("Remarkable files and folders tree:")
        display_tree(file_structure,'')
    if main_param=="sync":
        has_good_param=True
        print("Importing metadata from Remarkable ...")
        exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" root@10.11.99.1:~/.local/share/remarkable/xochitl/*.metadata ./metadata/')
        if exit_code!=0:
            print("Sync failed, check the remarkable is connected to a usb port, switched on and the provided password is the right one.")
            print("The data displayed in the system may be outdated until the problem is fixed.")
        print("Downloading PDFs from Remarkable ...")
        exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" root@10.11.99.1:~/.local/share/remarkable/xochitl/*.pdf ./pdf/')
        if exit_code!=0:
            print("Sync failed, check the remarkable is connected to a usb port, switched on and the provided password is the right one.")
            print("The data displayed in the system may be outdated until the problem is fixed.")
    if main_param=="password":
        has_good_param=True
        if main_param_param1=="":
            print("Usage: Pyram password <password>")
        else:
            with open('./passwd.rm','w') as pfile:
                pfile.write(main_param_param1)
                pfile.close()
    if main_param=="export":
        has_good_param=True
        if main_param_param1=="" or main_param_param2=="":
            print("Usage: Pyrem export <path to file on remarkable> <local folder>")
        else:
            file_path = main_param_param1.split('/')
            c_dir = ''
            dir_found=True
            for i in range(1,len(file_path)-1):
                bool_array = file_structure[:,0]==c_dir
                current_folder_files = file_structure[bool_array]
                bool_target = current_folder_files[:,2]==file_path[i]
                target_folder = current_folder_files[bool_target]
                if target_folder.size==0:
                    print("Invalid path to file on remarkable")
                    dir_found=False
                    break
                else:
                    c_dir=target_folder[0][1]
            if dir_found==True:
                bool_array = file_structure[:,0]==c_dir
                current_folder_files = file_structure[bool_array]
                bool_target = current_folder_files[:,2]==file_path[len(file_path)-1]
                target_file = current_folder_files[bool_target]
                if target_file.size==0:
                    print("File not found on remarkable.")
                else:
                    if os.path.exists('./pdf/'+target_file[0][1]+'.pdf') == False:
                        print('Export works only with PDFs ... for now :-) ')
                    else:
                        if main_param_param2.endswith('/'):
                            exit_code=os.system('cp ./pdf/'+target_file[0][1]+'.pdf '+main_param_param2+target_file[0][2]+'.pdf')
                        else:
                            exit_code=os.system('cp ./pdf/'+target_file[0][1]+'.pdf '+main_param_param2+'/'+target_file[0][2]+'.pdf')
                        if exit_code!=0:
                            print("Export failed, please check that output directory exists.")
                        else:
                            print("File exported.")
    if main_param=="import":
        has_good_param=True
        print("Importing file to Remarkable ...")
        new_uuid=subprocess.check_output(['/usr/bin/sshpass','-p',remarkable_password,'ssh','-o','StrictHostKeyChecking=no','root@10.11.99.1',"'uuidgen'"])
        new_uuid=new_uuid.decode("utf-8") 
        new_uuid=new_uuid[:-1]
        if os.path.exists(main_param_param1)==False:
            print("The file to import does not exist.")
        else:
            if main_param_param1.endswith(".pdf")==False:
                print("The file to import must be a PDF.")
            else:
                path_split = main_param_param1.split('/')
                pdf_name = path_split[len(path_split)-1]
                print(pdf_name+" ----> "+new_uuid+".pdf")
                exit_code=os.system('cp '+main_param_param1+' ./pdf/'+new_uuid+'.pdf')
                metadata_file = ['{']
                metadata_file.append('    "lastModified": "1684385173606",')
                metadata_file.append('    "lastOpened": "1688114359369",')
                metadata_file.append('    "lastOpenedPage": 0,')
                metadata_file.append('    "parent": "",')
                metadata_file.append('    "pinned": false,')
                metadata_file.append('    "type": "DocumentType",')
                metadata_file.append('    "visibleName": "'+pdf_name+'"')
                metadata_file.append('}')
                with open('./metadata/'+new_uuid+'.metadata','w') as pfile:
                    pfile.writelines(metadata_file)
                    pfile.close()
                content_file = ['{']
                content_file.append('    "extraMetadata": {')
                content_file.append('    },')
                content_file.append('    "fileType": "pdf",')
                content_file.append('    "fontName": "",')
                content_file.append('    "lastOpenedPage": 0,')
                content_file.append('    "lineHeight": -1,')
                content_file.append('    "margins": 100,')
                content_file.append('    "pageCount": 1,')
                content_file.append('    "textScale": 1,')
                content_file.append('    "transform": {')
                content_file.append('        "m11": 1,')
                content_file.append('        "m12": 1,')
                content_file.append('        "m13": 1,')
                content_file.append('        "m21": 1,')
                content_file.append('        "m22": 1,')
                content_file.append('        "m23": 1,')
                content_file.append('        "m31": 1,')
                content_file.append('        "m32": 1,')
                content_file.append('        "m33": 1')
                content_file.append('    }')
                content_file.append('}')
                with open('./content/'+new_uuid+'.content','w') as pfile:
                    pfile.writelines(metadata_file)
                    pfile.close()
                exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" ./pdf/'+new_uuid+'.pdf root@10.11.99.1:~/.local/share/remarkable/xochitl/')
                if exit_code!=0:
                    print("Import failed.")
                exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" ./metadata/'+new_uuid+'.metadata root@10.11.99.1:~/.local/share/remarkable/xochitl/')
                if exit_code!=0:
                    print("Import failed.")
                exit_code=os.system('rsync -e "/usr/bin/sshpass -p '+remarkable_password+' ssh -o StrictHostKeyChecking=no -l root" ./content/'+new_uuid+'.content root@10.11.99.1:~/.local/share/remarkable/xochitl/')
                if exit_code!=0:
                    print("Import failed.")
                os.system("/usr/bin/sshpass -p "+remarkable_password+" ssh -o StrictHostKeyChecking=no root@10.11.99.1 'systemctl restart xochitl'")

         


    
    if param_start=="help" or has_good_param==False:
        print("PyRem usage:")
        print("    pyrem.py sync: synchronize data from the remarkable")
        print("    pyrem.py tree: display the full files and folders tree")
        print("    pyrem.py password <pasword>: store the remarkable password")
        print("    pyrem.py export <path to file on remarkable> <local folder> export the file to the local path")
        print("    pyrem.py import <local path to the PDF to import")
    


if __name__ == "__main__":
    main()
