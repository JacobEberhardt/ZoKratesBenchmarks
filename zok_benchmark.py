#!/usr/bin/env python
# coding: utf-8

# ### Compilation/Generation Benchmark:
# 
# #### Requirements for running:
# - ZoKrates installed (via install script)
# 
# 
# #### Select files:
# - Drop all files that are supposed to be benchmarked in the files/ directory in this project
# 
# #### Python Imports:

# In[1]:


get_ipython().run_cell_magic('capture', '', 'import sys\n!{sys.executable} -m pip install matplotlib\n!{sys.executable} -m pip install numpy\n!{sys.executable} -m pip install csv2md\nimport os\nimport math\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport datetime\nimport statistics')


# #### Iterate Files:
# 
# ##### Benchmark Settings:
# - Each programm will be run N * R times
#     - N: Number of loop iterations. The minimum value of all loop execution times is returned to eliminate side-effects from parallel processes on the benchmarking machine.
#     - R: Number of repetitions in one loop. Values are averaged, stddev is calculated.

# In[ ]:


compile_opt = []
compile_opt_stdev = []
setup_opt = []
setup_opt_stdev = []
witness_opt = []
witness_opt_stdev = []
proof_opt = []
proof_opt_stdev = []
constraints_opt = []
compile_unopt = []
compile_unopt_stdev = []
setup_unopt = []
setup_unopt_stdev = []
witness_unopt = []
witness_unopt_stdev = []
proof_unopt = []
proof_unopt_stdev = []
constraints_unopt = []
mem_usg = []
mem_usg_stdev = []
files = []
started = 0

# Set N and R here, also set in alias_magic!!
n = 5
r = 3
get_ipython().run_line_magic('alias_magic', 'benchmark timeit -p "-n 5 -r 3 -o"')

def compile_file(file, unopt):
    if unopt:
        cmd = f"./memusg.sh ./zokrates_unoptimized compile -i files/{file} --light > constraints.txt"
        value = get_ipython().run_line_magic('benchmark', '!{cmd}')
        compile_unopt.append(int(value.best * 1000000))
    else:
        cmd = f"./memusg.sh zokrates compile -i files/{file} --light > constraints.txt"
        value = get_ipython().run_line_magic('benchmark', '!{cmd}')
        compile_opt.append(int(value.best * 1000000))
    get_memusg()

def setup(unopt):
    if unopt:
        cmd = f"./memusg.sh ./zokrates_unoptimized setup --light >> console_log.txt"
        value = get_ipython().run_line_magic('benchmark', '!{cmd}')
        setup_unopt.append(int(value.best * 1000000))
    else:
        cmd = f"./memusg.sh zokrates setup --light >> console_log.txt"
        value = get_ipython().run_line_magic('benchmark', '!{cmd}')
        setup_opt.append(int(value.best * 1000000))
    get_memusg()

def witness(file, unopt):
    params = get_parameters(file)
    if unopt:
        cmd = f"./memusg.sh ./zokrates_unoptimized compute-witness {params} --light >> console_log.txt"
        value = get_ipython().run_line_magic('benchmark', '!{cmd}')
        witness_unopt.append(int(value.best * 1000000))
    else:
        cmd = f"./memusg.sh zokrates compute-witness {params} --light >> console_log.txt"
        value = get_ipython().run_line_magic('benchmark', '!{cmd}')
        witness_opt.append(int(value.best * 1000000))
    get_memusg()

def proof(unopt):
    if unopt:
        cmd = f"./memusg.sh ./zokrates_unoptimized generate-proof >> console_log.txt";
        value = get_ipython().run_line_magic('benchmark', '!{cmd};')
        proof_unopt.append(int(value.best * 1000000))
    else:
        cmd = f"./memusg.sh zokrates generate-proof >> console_log.txt";
        value = get_ipython().run_line_magic('benchmark', '!{cmd};')
        proof_opt.append(int(value.best * 1000000))
    get_memusg()

# counts constraints by looking into out.ztf
def count_constraints(unopt):
    f = open("./constraints.txt",'r')
    lines = f.read().splitlines()
    length = lines[-1].split("Number of constraints: ")[1]
    if unopt:
        constraints_unopt.append(length)
    else:
        constraints_opt.append(length)
    
    
def get_memusg():
    with open('exports/data/memusg_res.txt', 'r+') as f:
        val_list = [int(line.rstrip()) for line in f]
        chunks = [val_list[x:x+r] for x in range(0, len(val_list), r)] # turns list into list of repetitions results -> dim: [n][r]
        mem_usg.append(min([statistics.mean(chunk) for chunk in chunks])) # takes average of each loop and selects min as result
        f.truncate(0)

'''
this method gets the first line of given .zok file and extracts function parameters.
Expected format: 
    -commented out in first line of file with a space after '//'

E.g.

// 337 113569
def main(private field a, field b) -> (field):
  field result = if a * a == b then 1 else 0 fi
  return result
'''
def get_parameters(file):
    with open('files/' + file) as f:
        line = f.readline()
        if "//" in line:
            return "-a" + line.replace("//", "")
        else:
            return ""

# empties files from previous results
def reset_files():
    results = open("exports/data/result.csv", "w")
    results.write("file, compile_opt_microsec, memusg_compile_KiB, setup_opt_microsec, memusg_setup_KiB, witness_opt_microsec, memusg_witness_KiB, proof_opt_microsec, memusg_proof_KiB, constr_opt, compile_unopt_microsec, memusg_compile_KiB, setup_unopt_microsec, memusg_setup_KiB, witness_unopt_microsec, memusg_witness_KiB, proof_unopt_microsec, memusg_proof_KiB, constr_unopt\n")
    open("exports/data/memusg_res.txt", 'w').close()
    open("console_log.txt", 'w').close()
    
    
    
def export_data():
    file = open("exports/data/result.csv", "a")
    for i, val in enumerate(compile_opt):
        file.write(
            files[i] + ", " +
            str(val) + ", " + 
            str(mem_usg[i]) + ", " + 
            str(setup_opt[i]) + ", " +
            str(mem_usg[(8 * i) + 1]) + ", " + 
            str(witness_opt[i]) + ", " + 
            str(mem_usg[(8 * i) + 2]) + ", " + 
            str(proof_opt[i]) + ", " + 
            str(mem_usg[(8 * i) + 3]) + ", " + 
            str(constraints_opt[i]) + ", " +
            str(compile_unopt[i]) + ", " +  
            str(mem_usg[(8 * i) + 4]) + ", " + 
            str(setup_unopt[i]) + ", " + 
            str(mem_usg[(8 * i) + 5]) + ", " + 
            str(witness_unopt[i]) + ", " +  
            str(mem_usg[(8 * i) + 6]) + ", " + 
            str(proof_unopt[i]) + ", " + 
            str(mem_usg[(8 * i) + 7]) + ", " + 
            str(constraints_unopt[i]) + "\n"
        )
    file.close()
    
reset_files()  
for file in sorted(os.listdir('./files')):
    if file.endswith(".zok"):
        print(file)
        started = datetime.datetime.now() 
        print("Started Optimized: " + started.strftime("%H:%M:%S") + "\n")
        print("Compiling: ", end =" ")
        compile_file(file, False)
        print("Setup: ", end =" ")
        setup(False)
        print("Witness: ", end =" ")
        witness(file, False)
        print("Proof: ", end =" ")
        proof(False)
        print("\nRan: " + str(datetime.datetime.now() - started))
        count_constraints(False)
        print("_________________________________________________\n")
        started = datetime.datetime.now() 
        print("Started Unoptimized: " + started.strftime("%H:%M:%S") + "\n")
        print("Compiling: ", end =" ")
        compile_file(file, True)
        print("Setup: ", end =" ")
        setup(True)
        print("Witness: ", end =" ")
        witness(file, True)
        print("Proof: ", end =" ")
        proof(True)
        print("\nRan: " + str(datetime.datetime.now() - started))
        print("_________________________________________________\n")
        count_constraints(True)

    else:
        continue
    
    files.append(file.split('.')[0])

export_data()


# In[22]:


get_ipython().system('csv2md exports/data/result.csv > exports/data/table.md')

with open("exports/data/table.md") as f:
    print(f.read())


# #### Compilation and Setup Diagram:
# 

# In[ ]:


x = np.arange(len(constraints_opt))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, compile_opt, width, label='Compile', edgecolor='#005eb8', color='#7faedb')
rects2 = ax.bar(x + width/2, setup_opt, width, label='Setup', edgecolor='#ff4c4c', color='#ffa5a5')
ax.set_ylabel('t in μs')
ax.set_xticks(x)
ax.set_xlabel('# of Constraints')
ax.set_xticklabels(constraints_opt)
ax.legend()
ax.semilogy(np.exp(0 / max(setup_opt)))
ax.set_ylim(ymin=1000)
fig.tight_layout()
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = "#cccccc"
plt.savefig('exports/compile-setup.png')
plt.show()


# #### Witness and Proof Diagram:

# In[ ]:


x = np.arange(len(constraints_opt))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, witness_opt, width, label='Witness', edgecolor='#005eb8', color='#7faedb')
rects2 = ax.bar(x + width/2, proof_opt, width, label='Proof', edgecolor='#ff4c4c', color='#ffa5a5')
ax.set_ylabel('t in μs')
ax.set_xticks(x)
ax.set_xlabel('# of Constraints')
ax.set_xticklabels(constraints_opt)
ax.legend()
ax.semilogy(np.exp(0 / max(setup_opt)))
ax.set_ylim(ymin=1000)
fig.tight_layout()
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = "#cccccc"
plt.savefig('exports/witness-proof.png')
plt.show()


# In[ ]:





# In[ ]:




