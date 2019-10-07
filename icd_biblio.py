# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 19:31:06 2019

@author: Kryzhevoi
"""

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# read data from  csv-file and clean 
df = pd.read_csv('icd.bibl_19092019.csv', encoding = "utf-8")  
df.rename(columns={'Identifier':'Id'}, inplace=True) 
df.Journal = df.Journal.str.strip() 
df.Note = df.Note.str.strip() 
mapping = {'theory':'Theory','experiment':'Experiment','experiment & theory':'Joint Works'}
df.Note = df.Note.map(mapping)
icd_bibl = df[['Id', 'Author', 'Year', 'Journal', 'Note']]

# some statistics
n_entries = len(icd_bibl) 
years = icd_bibl['Year'].unique()
journals = icd_bibl['Journal'].nunique()

publ_cat = icd_bibl.groupby('Note')['Id'].count().sort_values(ascending=False)
publ_cat_dict = publ_cat.to_dict()

auth_recs = icd_bibl['Author'].values
all_authors = []
for rec in auth_recs:
    a_list = rec.replace(' &', ';').split(';')
    for i in range(len(a_list)):
        all_authors.append(a_list[i].split('.')[0].strip(' '))
author_count_ser = pd.Series(all_authors).value_counts()
###########

def print_basic_stats():
    print("Found ....")
    print("      Entries: {}".format(n_entries))
    print("      Papers by categories:",', '.join(['{}'] * 3).format(*publ_cat_dict.items()))
    print("      Publication years: {min} -- {max}".format(min=years.min(), max=years.max()))
    print("      Distinct journals: {}".format(journals))
    print("      Distinct authors: {}".format(len(author_count_ser)))
    print("      ....")
    return
    

def create_publs_over_years(): #create fig "icd.publs_over_years.png"
    publ_year = icd_bibl.groupby('Year')['Id'].count()
    yy_span = len(years)

    plt.style.use('seaborn-darkgrid')
    sns.set_context("poster")

    fig, ax = plt.subplots(figsize=(23,8), dpi=100)
#plot
    ax.bar(range(yy_span), publ_year)
#tics
    ax.set_xticks(range(yy_span))
    ax.set_xticklabels(years)
    ax.set_xlim(-1, yy_span)
    ax.set_ylim(0, 31)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
#labels and title
    plt.xlabel('Year', fontsize=30, labelpad=15)
    plt.ylabel('Publications', fontsize=30, labelpad=15)
    plt.title('Publications over Years', fontsize=35)
    ax.title.set(y=1.05)
#save to file
    plt.savefig("icd.publs_over_years.png", transparent=False, \
                bbox_inches='tight', padinches=1) 
    fig.clf()
    return


def create_publs_by_cat(): #create fig "icd.publs_by_category.png"
    plt.style.use('seaborn-whitegrid')
    sns.set_context("poster")

    fig1, ax1 = plt.subplots(figsize=(10,8))
# plot
    explode = (0.0, 0.0, 0.0)
    ax1.pie(publ_cat, explode=explode, \
        autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, p * n_entries/100), \
        shadow=True, startangle=-80, radius=1, \
        wedgeprops=dict(width=0.7, edgecolor='w', linewidth=1.0), \
        textprops={'fontsize': 25, 'color': 'w'})
#legend
    ax1.legend(publ_cat.index, loc="right", fontsize=20, bbox_to_anchor=(0, 0, 1.3, 1))
#axis and title
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Papers by Category', fontsize=39)
#save to file
    plt.savefig("icd.publs_by_category.png", transparent=False, \
                bbox_inches='tight', padinches=1)
    fig1.clf()
    return


def create_publs_by_journal(): #create icd.publs_by_journal.png
    publ_jour = icd_bibl.groupby('Journal')['Id'].count().reset_index()
    publ_jour_sort = publ_jour.sort_values(by=['Id','Journal'], ascending=[False,True]).reset_index(drop=True)
#    print(pap_jour_sort)
    n_others = publ_jour_sort.iloc[26:].sum()
    new_row = pd.DataFrame({"Journal": ["Others"], "Id": [n_others[1]]})
    publ_jour_fin = publ_jour_sort.iloc[:26].append(new_row, ignore_index=True)
#    print(pap_jour_fin)
    jour_names = publ_jour_fin['Journal'].values
    
    plt.style.use('seaborn-darkgrid')
    sns.set_context("notebook")

    fig2, ax2 = plt.subplots(figsize=(22,8))
#plot
    ax2.barh(range(27), publ_jour_fin['Id'])
#tics
    ax2.set_yticks(range(27))
    ax2.set_yticklabels(jour_names)
    ax2.set_ylim(26.7, -0.7)
    ax2.set_xticks(range(0, 61, 5))
    ax2.set_xlim(-1,60)
    plt.xticks(fontsize=15)
#plt.yticks(fontsize=40)
    ax2.xaxis.set_label_coords(0.45, -0.08)

#labels and title
    plt.xlabel('Publications', labelpad=15, fontsize=20)
    plt.title('Publications by Journal', fontsize=20)
    ax2.title.set(y=1.02, x=0.42)

#save to file
    plt.savefig("icd.publs_by_journal.png", transparent=False, \
                bbox_inches='tight', padinches=1)
    fig2.clf()
    return


def create_coauthors_distr(): # create fig "icd.coathors_distr.png"
    auths_by_cat = [icd_bibl[icd_bibl['Note'] == cat]['Author'] for cat in publ_cat.index] 
#    print(auths_by_cat)
    auths_by_cat_nums = []
    for cat in auths_by_cat:
        nums = [len(authors.replace(' &', ';').split(';')) for authors in cat]
        auths_by_cat_nums.append(nums)
#    print(auths_by_cat_nums)
    
    plt.style.use('seaborn-whitegrid')
    sns.set_context("poster")

    fig4, ax4 = plt.subplots(figsize=(10.5,9.5))

    #plot
    sns.boxplot(data=auths_by_cat_nums, notch=False)
    #ticks
    cat_labels = publ_cat.index
    ax4.set_xticks(range(3))
    ax4.set_xticklabels(cat_labels)
    ax4.set_yticks(range(0,52,5))
    ax4.set_ylim(0,52)
    plt.xticks(fontsize=23)
    plt.yticks(fontsize=23)
    #labels and title
    plt.ylabel('Co-authors', fontsize=35, labelpad=15) 
    plt.xlabel('Paper Category', fontsize=35, labelpad=15)
    plt.title("Co-authors by Paper Category", fontsize=39)
    ax4.title.set(y=1.05)
    #save to file
    plt.savefig("icd.coathors_distr.png", transparent=False, \
                bbox_inches='tight', padinches=1)  
    fig4.clf()
    return


def create_top10(): # create fig "icd.top10.png"
    author_count_df = pd.DataFrame({'Author': author_count_ser.index, 'Counts': author_count_ser.values})    
    top10_authors = ["Kolorenč" if author_count_df.iat[i,0].split(',')[0] == "Koloren\\v{c}" 
                     else author_count_df.iat[i,0].split(',')[0] for i in range(10)]
    top10_scores = [author_count_df.iat[i,1] for i in range(10)]
#    print(top10_authors, top10_scores)
    
    #20 authors by category (1:Theory, 2:Experiment)
    auths_cat = {'Cederbaum':1, 'Gokhberg':1, 'Jahnke':2, 'Schöffler':2, 'Dörner':2, 
                 'Ueda':2, 'Kuleff':1, 'Kolorenč':1, 'Hergenhahn':2, 'Kryzhevoi':1, 
                 'Sisourat':1, 'Fukuzawa':2, 'Saito':2, 'Averbukh':1, 'Schmidt-Böcking':2, 
                 'Liu':2, 'Demekhin':1, 'Trinter':2, 'Santra':1, 'Czasch':2}
#
    plt.style.use('seaborn-darkgrid')
    sns.set_context("poster")

    fig5, ax5 = plt.subplots(figsize=(25,8))
    
    indices1 = [i for i in range(10) if auths_cat[top10_authors[i]] == 1] #theory
    indices2 = [i for i in range(10) if auths_cat[top10_authors[i]] == 2] #experiment
#    print(indices1)
#    print(indices2)
    # Create bars
    barWidth = 0.8
    bars1 = [top10_scores[i] for i in indices1]
    bars2 = [top10_scores[i] for i in indices2] 
    # Create barplot
    plt.bar(indices1, bars1, width = barWidth, color = ['royalblue']*len(indices1), label='Theory')
    plt.bar(indices2, bars2, width = barWidth, color = ['darkorange']*len(indices2), label='Experiment')
    # Create legend
    plt.legend(fontsize=25)
    # ticks
    plt.xticks([r for r in range(10)], [i for i in top10_authors], rotation=0, fontsize=24)
    ax5.set_xlim(-0.7,9.7)
    plt.yticks(fontsize=24)
    # labels and title
    plt.xlabel('Author', fontsize=33, labelpad=15)
    plt.ylabel('Publications', fontsize=33, labelpad=15)
    plt.title('Top 10 Authors', fontsize=39)
    ax5.title.set(y=1.05)
    #save to file
    plt.savefig("icd.top10.png", transparent=False, bbox_inches='tight', padinches=1)
    fig5.clf()   
    return


#print(icd_bibl.head())
print_basic_stats()  
create_publs_over_years() 
create_publs_by_cat()
create_publs_by_journal()
create_coauthors_distr()
create_top10()
#plt.show()
