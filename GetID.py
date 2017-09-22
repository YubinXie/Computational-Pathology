import os


folder="../Rawinput/SelectedTissue_2"
files = [file.replace(".jpg",".svs") for file in os.listdir(folder) if "jpg" in file]
with open ("Selected.txt","w") as OpenOutput:
	for file in files:
		OpenOutput.writelines(file+"\n")
