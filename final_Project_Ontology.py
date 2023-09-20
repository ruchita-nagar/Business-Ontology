import io
import nltk
import string
import re
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from collections import OrderedDict

#Extract Text from PDF using PDFMiner
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text
    
#Driver Code
if __name__ == '__main__':
    all_text = extract_text_from_pdf('business_new.pdf')#path of pdf file
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(all_text) 
    filtered_sentence = [] #to store extracted text.
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w.lower()) 
    filtered_sentence = [''.join(c for c in s if c not in string.punctuation and not c.isdigit()) for s in filtered_sentence]
    filtered_sentence = [ele for ele in filtered_sentence if ele != "" and len(ele)>3]        
    filtered_sentence = [w for w in filtered_sentence if not w in stop_words] 
    #print(filtered_sentence)
    
    
    is_noun = lambda pos: pos[:2] == 'NN'
    nouns = [word for (word, pos) in nltk.pos_tag(filtered_sentence) if is_noun(pos)] 
    print(len(set(nouns)))

    freq = nltk.FreqDist(nouns) 
    
    nounDictonery={}
    for key,val in freq.items(): 
       nounDictonery[key]=val
    nounDictonery = OrderedDict(sorted(nounDictonery.items(), key=lambda x: x[1],reverse=True))
    #print(nounDictonery)
    
    freq.plot(50,cumulative=False)
    
    # print(nounDictonery)
    file=open("final1.txt",'w')
    for i in sorted(nounDictonery.items(),key=(lambda x:(x[1],x[0])),reverse=True):
        if i[1]<3:
            break
        file.write(str(i[0]))
        file.write(" ")
        file.write(str(i[1]))
        file.write('\n')
    file.close()
    
    regxpfile=open("SET_OF_REGULAR_XP.txt","r")
    myregxp=regxpfile.read()
    #print(len(myregxp.split('\n')))
    #print("\n".join([reg for reg in myregxp.split('\n')]))
    #print('########################################################\n'*2)
    for regxp in myregxp.split('\n')[0:-2]:
        string=r"{0}".format(regxp)
        pattern=re.compile(string)
        find=pattern.findall(all_text)
        #print(find)
        #print('##########################################'*3)

    regxpfile.close()
    
    list_of_all_files=[]
    regxpfile=open("SET_OF_REGULAR_XP.txt","r")
    myregxp=regxpfile.read()
    for regxp in myregxp.split('\n')[0:-2]:
        string=r"{0}".format(regxp)
        pattern=re.compile(string)
        find=pattern.findall(all_text)
        file_name=regxp[8:-2]+"2.txt"
        list_of_all_files.append(file_name)
        temp=open(file_name,"w")
#       print(file_name)
        lt=[]
        for i in find:
            string1=i.split()[0]
            word=nltk.word_tokenize(string1)
            nltk.pos_tag(word)
            if string1 not in stop_words and string1 not in lt and len(string1)>3 and nltk.pos_tag(word)[0][1]!='VB'and nltk.pos_tag(word)[0][1]=='NN':
               # print(string1)
                temp.write(string1+"_"+i.split()[1]+"\n")
                lt.append(string1)
        lt.clear()
        temp.close()
        
    regxpfile.close()
    #print(list_of_all_files)
    
    
    header='''<?xml version = '1.0' encoding = 'UTF-8'?>
    <Ontology xmlns="http://www.w3.org/2002/07/owl#" xml:base="http://www.ontorion.com/ontologies/Ontologyc03a901c68d84461b4657ce45cc0e86c#" ontologyIRI="http://www.ontorion.com/ontologies/Ontologyc03a901c68d84461b4657ce45cc0e86c#">'''
    onto=open('business.owl','w')
    onto.write(header+"\n")
    onto.close()
    for parent in list_of_all_files[:-2]:
        file1=open(parent,"r")
        #print("New_Parent")
        childs=file1.read().split("\n")
        #print(childs)
        for child in childs[:-1]:
            gt="\n\n\n<SubClassOf>\n<Class IRI="+'\"'+child+'\"'+" />\n<Class IRI="+'\"'+parent[:-5]+'\"'+" />\n</SubClassOf>\n\n"
            ct="<SubClassOf>\n<Class IRI="+'\"'+child+'\"'+" />\n<ObjectSomeValuesFrom>\n<ObjectProperty IRI="+'\"'+"is_type_of"+'\"'+" />\n<Class IRI="+'\"'+parent[:-5]+'\"'+" />\n</ObjectSomeValuesFrom>\n</SubClassOf>\n"
            with io.open("business.owl", "a", encoding="utf-8") as f1:
                f1.write(str(gt))
                f1.write("\n")
                f1.write(str(ct))

    with io.open("business.owl", "a", encoding="utf-8") as f1:
            f1.write('''\n\n</Ontology>''')