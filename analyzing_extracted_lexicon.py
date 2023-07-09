from pymetamap import MetaMap

# Import os to make system calls
import os

# For pausing
from time import sleep
from tqdm import tqdm

# Setup UMLS Server
metamap_base_dir = '~/public_mm/'
metamap_bin_dir = 'bin/metamap20'
metamap_pos_server_dir = 'bin/skrmedpostctl'
metamap_wsd_server_dir = 'bin/wsdserverctl'

# Start servers
os.system(metamap_base_dir + metamap_pos_server_dir + ' start') # Part of speech tagger
os.system(metamap_base_dir + metamap_wsd_server_dir + ' start') # Word sense disambiguation 

# Sleep a bit to give time for these servers to start up
sleep(30)

print("Servers ready")

def get_keys_from_mm(concept, klist):
    conc_dict = concept._asdict()
    conc_list = [conc_dict.get(kk) for kk in klist]              
    return(tuple(conc_list))

english_biomed_gazetteer = open("english_biomed_gazetteer.txt", encoding="utf-8", mode = "w")
lexiconStatic_base_extracted = open("lexiconStatic_base_extracted.txt", encoding="utf-8", mode = "r")

dat = list(map(lambda x : x.strip(), lexiconStatic_base_extracted.readlines()))
print("Check 1")

preferred_names = []
metam = MetaMap.get_instance("/home/ayat/public_mm/bin/metamap20")

'''Semantic Types
acab|T020|Acquired Abnormality
anab|T190|Anatomical Abnormality
anst|T017|Anatomical Structure
antb|T195|Antibiotic
bacs|T123|Biologically Active Substance
bdsu|T031|Body Substance
blor|T029|Body Location or Region
bpoc|T023|Body Part, Organ, or Organ Component
bsoj|T030|Body Space or Junction
cgab|T019|Congenital Abnormality
chem|T103|Chemical
chvf|T120|Chemical Viewed Functionally
chvs|T104|Chemical Viewed Structurally
clnd|T200|Clinical Drug
diap|T060|Diagnostic Procedure
dsyn|T047|Disease or Syndrome
enzy|T126|Enzyme
ffas|T021|Fully Formed Anatomical Structure
hops|T131|Hazardous or Poisonous Substance
horm|T125|Hormone
inch|T197|Inorganic Chemical
irda|T130|Indicator, Reagent, or Diagnostic Aid
lbpr|T059|Laboratory Procedure
mbrt|T063|Molecular Biology Research Technique
orch|T109|Organic Chemical
topp|T061|Therapeutic or Preventive Procedure
vita|T127|Vitamin


'''

window = 5000
for idx in tqdm(range(0, len(dat), window)):
    dat_slice = dat[idx : idx + window]
    cons, errs = metam.extract_concepts(dat_slice,
                                    word_sense_disambiguation = True,
                                    #restrict_to_sts = ['dsyn', 'anst', 'sosy', 'antb', 'bacs', ], 
                                    composite_phrase = 1, # for memory issues
                                    prune = 30)
    for con in cons:
        conc_dict = con._asdict()
        if conc_dict.get("preferred_name") not in preferred_names:
            english_biomed_gazetteer.write(conc_dict.get("preferred_name") + "~" + conc_dict.get("semtypes")[1:-1] + "\n")
            preferred_names.append(conc_dict.get("preferred_name"))

print("Check 2")
