import os
import sys
sys.path.append('/home/zjg/.local/Lib/site-packages/')
import os
import sys
import pandas as pd
import numpy as np
from os.path import join, getsize

print(os.path.abspath('../../'))
sys.path.append(os.path.abspath('../../'))
from pubmed.parser.pubmed_xml_parser import PubmedXmlParser

focused_type = [
   'Randomized Controlled Trial', 
   'Clinical Trial',
   'Observational Study',
   'Controlled Clinical Trial',
   'Clinical Trial, Phase II',
   'Clinical Trial, Phase I',
   'Clinical Trial, Phase III',
   'Clinical Trial Protocol',
   'Clinical Study',
   'Randomized Controlled Trial, Veterinary',
   'Clinical Trial, Phase IV',
   'Pragmatic Clinical Trial',
   'Clinical Trial, Veterinary',
   'Equivalence Trial',
   'Adaptive Clinical Trial'
]

def _has_pmc_free_article(full_links):
   for full_link in full_links:
      if full_link['idType'] == 'pmc':
         return True
   return False

def _has_clinical_trial_link(databanks):
   for databanks in databanks:
      if databanks['databank_name'] == 'ClinicalTrials.gov':
         return True
   return False

def _is_clinical_trials_type(publication_types):
   for publication_type in publication_types:
      if publication_type.get('text', '') in focused_type:
         return True
   return False

def filter_clinical_trials_type(publication_types):
   result = []
   for publication_type in publication_types:
      if publication_type.get('text', '') in focused_type:
         result.append(publication_type)
   return result
def get_journal_year(article_journal):
   journal_year = article_journal.get('JournalIssue_PubDate_Year', "")
   if journal_year:
      return journal_year
   else:
      medlinedate =  article_journal.get('JournalIssue_PubDate_MedlineDate', "")
      if medlinedate:
         return medlinedate[0:4]
   return ''

dir_root = "/home/zjg/code3.31/xmlpubmed"
pmid_info = {}
file_names = os.listdir(dir_root)
file_names.sort()
results = []
size =0

"""for file_name in file_names:
   if(getsize('/home/zjg/code3.31/xmlpubmed/'+file_name)!=0):
      if os.path.isfile(os.path.join(dir_root, file_name)) and 'xml.gz' in file_name:
         result_path = os.path.join(dir_root, file_name)
         dict_out = PubmedXmlParser.parse_pubmed_xml_gz(result_path)"""
for i in range(0,200):
   print(file_names[i])
   if(getsize( "/home/zjg/code3.31/xmlpubmed/"+file_names[i])!=0):
      if os.path.isfile(os.path.join(dir_root, file_names[i])) and 'xml.gz' in file_names[i]:
         result_path = os.path.join(dir_root, file_names[i])
         dict_out = PubmedXmlParser.parse_pubmed_xml_gz(result_path)

         
         articles = dict_out['articles']
         
         for article in articles:
            
            pmid = PubmedXmlParser.parse_pmid(article)
            doi = PubmedXmlParser.parse_doi(article)
            full_links = PubmedXmlParser.parse_article_links(article)
            databank = PubmedXmlParser.parse_databanks(article)
            article_journal = PubmedXmlParser.parse_article_journal(article)
            publication_types = PubmedXmlParser.parse_publication_types(article)
         
            is_clinical_trials_type = _is_clinical_trials_type(publication_types)
            has_pmc_free_article = _has_pmc_free_article(full_links)
            has_clinical_trial_link = _has_clinical_trial_link(databank)
            clinical_trials_types = filter_clinical_trials_type(publication_types)
            journal_year = get_journal_year(article_journal)
            #print(journal_year)
            #if journal_year == '2019' or journal_year == '2020':
            if journal_year == '2013' or journal_year == '2014' or journal_year == '2015' or journal_year == '2016' or journal_year == '2017' or journal_year == '2018' or journal_year == '2019' or journal_year == '2020':              

               result  = PubmedXmlParser.pubmed_article_to_dict(article)
               filter_result = {
                  'pmid': result['pmid'],
                  'title': result['title'],
                  'abstract': result['abstract']
               }
               results.append(filter_result)
      #break
               
      
          

   
#if journal_year == '2013' or journal_year == '2014' or journal_year == '2015' or journal_year == '2016' or journal_year == '2017' or journal_year == '2018' or journal_year == '2019' or journal_year == '2020':              

df = pd.DataFrame(results)
results = np.array_split(df, 100)
for index, result in enumerate(results):
   result.to_json(f'./pm800-1000/pubmed_8_years_{index}.json', orient='records', lines=True, force_ascii=False)