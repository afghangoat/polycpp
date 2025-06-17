from itertools import product
import os
import re


###CONFIG
DEBUG_VERBOSE=False
###ENDCONFIG

EXCLUSION= "POLYCPP"
TYPES = ["int", "double","char","void","float"]

def generate_functions(template_code):
    # This regex matches:
    #  - template<typename POLY_T, typename POLY_U>
    #  - the return type (e.g. POLY_T)
    #  - the function name (e.g. add)
    #  - the two parameters with both their types and names (e.g. POLY_T x1, POLY_U x2)
    #  - the function body (everything between { and })
    #  - followed by the marker end_template
    template_regex = re.compile(
        r"template\s*<\s*typename\s+(\w+)\s*,\s*typename\s+(\w+)\s*>\s*"
        r"(\w+)\s+(\w+)\s*\(\s*(\w+)\s+(\w+)\s*,\s*(\w+)\s+(\w+)\s*\)\s*"
        r"{(.*?)}\s*end_template",
        re.DOTALL
    )

    match = template_regex.search(template_code)
    if match:
        tparam1 = match.group(1)   # e.g., POLY_T
        tparam2 = match.group(2)   # e.g., POLY_U
        ret_type_template = match.group(3)
        func_name = match.group(4)
        param1_type_template = match.group(5)
        param1_name = match.group(6)
        param2_type_template = match.group(7)
        param2_name = match.group(8)
        body = match.group(9).strip()

        generated_code = []

        for concrete_t1, concrete_t2 in product(TYPES, repeat=2):
            specific_ret_type = ret_type_template.replace(tparam1, concrete_t1).replace(tparam2, concrete_t2)
            specific_param1_type = param1_type_template.replace(tparam1, concrete_t1).replace(tparam2, concrete_t2)
            specific_param2_type = param2_type_template.replace(tparam1, concrete_t1).replace(tparam2, concrete_t2)
            
            specific_func_name = f"{func_name}_{concrete_t1}_{concrete_t2}"
            
            func_def = (
                f"{specific_ret_type} {specific_func_name}({specific_param1_type} {param1_name}, "
                f"{specific_param2_type} {param2_name}) {{\n    {body}\n}}"
            )
            generated_code.append(func_def)
        
        return "\n\n".join(generated_code)
    else:
        print("No valid template found.")
        return None

def process_files_and_generate_functions(files):
    temptemplate=""
    intemp=False
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            new_lines = []

            for i, line in enumerate(lines):
                if "template<" in line and intemp==False:
                    intemp=True
                    temptemplate=""
                    temptemplate+=line
                elif intemp==False:
                    new_lines.append(line)
                
                if intemp==True:
                    temptemplate+=line
                if "end_template" in line:
                    intemp=False
                    temptemplate+=line
                    generated_code = generate_functions(temptemplate)
                    print(generated_code)
                    new_lines.append(generated_code)

            with open(file, 'w') as f:
                f.writelines(new_lines)

            print(f"Processed file: {file}")
        
        except FileNotFoundError:
            print(f"File {file} not found!")
        except Exception as e:
            print(f"An error occurred with file {file}: {e}")
        
def generate_generics(files):
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for i, line in enumerate(lines):
                if "<" in line and ">" in line:
                    new_lines=new_lines.replace("<","_")
                    new_lines=new_lines.replace(",","_")
                    idx=new_lines.index(">")
                    for n in range(0,idx):
                        if new_lines[n]==',':
                            new_lines[n]='_'
                    new_lines=new_lines.replace(">","")
                new_lines.append(line)

            with open(file, 'w') as f:
                f.writelines(new_lines)
        
        except FileNotFoundError:
            print(f"File {file} not found!")
        except Exception as e:
            if DEBUG_VERBOSE==True:
                print(f"An error occurred with file {file}: {e}")
    process_files_and_generate_functions(files)

def replace_colons(files):
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()

            content = content.replace('::', '.')

            with open(file, 'w') as f:
                f.write(content)
            if DEBUG_VERBOSE==True:
                print(f"Replaced '::' with '.' in {file}")
        except FileNotFoundError:
            print(f"File {file} not found!")
        except Exception as e:
            if DEBUG_VERBOSE==True:
                print(f"An error occurred with file {file}: {e}")

def append_transpilation(files,transpiler_init_code=""):
    found =False
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for i, line in enumerate(lines):
                if "int main(" in line and found==False:
                    found=True
                    new_lines.append(transpiler_init_code+"\n")
                    line+="\ninit_cpp_transpiler(); /*For transpiling pseudo CPP code*/\n"
                new_lines.append(line)

            with open(file, 'w') as f:
                f.writelines(new_lines)
            
            if DEBUG_VERBOSE==True:
                print(f"Inserted a line above 'int main(' in {file}")
        
        except FileNotFoundError:
            print(f"File {file} not found!")
        except Exception as e:
            if DEBUG_VERBOSE==True:
                print(f"An error occurred with file {file}: {e}")
    return found;

def get_class_init_code(files):
    in_class = False
    curclassname = ""
    class_init_code="";
    
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for i, line in enumerate(lines):
                if "class(" in line and not in_class:
                    if DEBUG_VERBOSE:
                        print("Class line found:", line.strip())
                    start_idx = line.index("class(") + len("class(")
                    end_idx = line.index(")", start_idx)
                    curclassname = line[start_idx:end_idx].strip()
                    in_class = True
                
                if in_class:
                    m = re.search(r'\(\*\s*([A-Za-z_]\w*)\s*\)', line)
                    if m:
                        curmethod = m.group(1)
                        print("Found", curmethod)
                        class_init_code += f"{curclassname}.{curmethod} = {curclassname}_{curmethod};\n"
                
                if in_class and "};" in line:
                    in_class = False

                new_lines.append(line)

            with open(file, 'w') as f:
                f.writelines(new_lines)

            if DEBUG_VERBOSE:
                print(f"Processed file: {file}")
        
        except FileNotFoundError:
            print(f"File {file} not found!")
        except Exception as e:
            if DEBUG_VERBOSE:
                print(f"An error occurred with file {file}: {e}")
    
    print("Generated class initialization code:")
    print(class_init_code)
    return class_init_code

def get_namespace_init_code(files):
    in_class = False
    curclassname = ""
    namespace_init_code="";
    
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for i, line in enumerate(lines):
                if "namespace(" in line and not in_class:
                    if DEBUG_VERBOSE:
                        print("Namespace line found:", line.strip())
                    start_idx = line.index("namespace(") + len("namespace(")
                    end_idx = line.index(")", start_idx)
                    curclassname = line[start_idx:end_idx].strip()
                    in_class = True
                
                if in_class:
                    m = re.search(r'\(\*\s*([A-Za-z_]\w*)\s*\)', line)
                    if m:
                        curmethod = m.group(1)
                        print("Found", curmethod)
                        namespace_init_code += f"{curclassname}.{curmethod} = {curclassname}_{curmethod};\n"
                
                if in_class and "end_namespace" in line:
                    in_class = False

                new_lines.append(line)

            with open(file, 'w') as f:
                f.writelines(new_lines)

            if DEBUG_VERBOSE:
                print(f"Processed file: {file}")
        
        except FileNotFoundError:
            print(f"File {file} not found!")
        except Exception as e:
            if DEBUG_VERBOSE:
                print(f"An error occurred with file {file}: {e}")
    
    print("Generated namespace initialization code:")
    print(namespace_init_code)
    return namespace_init_code

if __name__ == "__main__":
    files = input("Enter files separated by a ' ' (space): ").split()
    
    print("Transpilation (1/5) (Replacing ::-s...)\n")
    replace_colons(files)
    
    print("Transpilation (2/5) (Generating class init code...)\n")
    ccode=get_class_init_code(files)
    print("Transpilation (3/5) (Generating namespace init code...)\n")
    nscode=get_namespace_init_code(files)
    
    tp_code="void init_cpp_transpiler(){"+str(nscode)+" "+str(ccode)+"}";
    print("Transpilation (4/5) (Inserting transpiler init code...)\n")
    success=append_transpilation(files,tp_code)
    if success==True:
        if DEBUG_VERBOSE==True:
            print("Success")
    else:
        print("Inserting transpiler init code failed!! Fatal error!\n")
        
    print("Transpilation (5/5) (Inserting generics...)\n")
    generate_generics(files)
    
    print("Done! Transpilation complete!\n")