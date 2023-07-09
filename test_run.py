note1 = "Mrs. Jones came in today complaining of a lot of chest pain. She denies shortness of breath and fevers."

note2 = "Mr. Smith has been having pain in his knee for many weeks. It hurts when he walks. There is no swelling, erythema, or micromotion tenderness."

note3 = "Sandy Lemon has been having headaches for two months that are associated with blurry vision and numbness in her right arm."

# Put them all together in a list
note_list = [note1, note2, note3]

# Load MetaMap
from pymetamap import MetaMap

# Import os to make system calls
import os

# For pausing
from time import sleep

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

metam = MetaMap.get_instance("/home/ayat/public_mm/bin/metamap20")
#words = metam.get_words_by_semantic_type("SOSY")
# Set the semantic types to search for
semantic_types = ['sosy']

# Extract all concepts matching the specified semantic types
# cons, errs = metam.extract_concepts("",
#                                 word_sense_disambiguation = True,
#                                 restrict_to_sts = ['sosy'], # signs and symptoms
#                                 composite_phrase = 1, # for memory issues
#                                 prune = 30)

# Print the preferred names of the matched concepts
# print(len(cons))
# for concept in cons:
#     print(concept.preferred_name)

note_list = ["dyspnea"]

cons, errs = metam.extract_concepts(note_list,
                                word_sense_disambiguation = True,
                                restrict_to_sts = ['sosy'], # signs and symptoms
                                composite_phrase = 1, # for memory issues
                                prune = 30)
                                
import pandas as pd

def get_keys_from_mm(concept, klist):
    conc_dict = concept._asdict()
    conc_list = [conc_dict.get(kk) for kk in klist]              
    return(tuple(conc_list))
        
        
keys_of_interest = ['preferred_name', 'cui', 'semtypes', 'pos_info']
cols = [get_keys_from_mm(cc, keys_of_interest) for cc in cons]
results_df = pd.DataFrame(cols, columns = keys_of_interest)

# See results
print(results_df)