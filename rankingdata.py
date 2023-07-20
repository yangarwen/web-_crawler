from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time

url = 'https://www.shanghairanking.com/rankings/gras/2022'
driver = webdriver.Chrome()
driver.get(url)


#Get subject list & link url----------------------------------------------
subject_list = []
subject_area_map = {}
soup = BeautifulSoup(driver.page_source, "lxml")
subject_areas = soup.select(".subject-item")
for a in subject_areas:
    subject_area = a.contents[0].text.lstrip().rstrip()
    subjects = a.contents[2]
    for sub in subjects:
        subject = sub.contents[0].contents[0].text
        href = sub.find('a').get('href')
        href = 'https://www.shanghairanking.com'+ href
        subject_list.append(subject)
        subject_area_map[subject] = [subject_area, href]        
#print(subject_area_map)



#Get page's information-------------------------------------------------------
def get_a_page_data(soup):
    #Get page's information:university name, overall rank and score ---
    items = soup.find_all("tr")
    for row in items[1:]:
        # institution name
        uni_names = row.select('.univ-name') or row.select('.univ-name-normal')
        for uni in uni_names:
            uni_name = uni.text.lstrip().rstrip()
            unilist['Institution_Name'].append(uni_name)
        # overall rank and score
        rank = row.contents[0].text.lstrip().rstrip()
        score = row.contents[3].text.lstrip().rstrip()
        unilist['Rank'].append(rank)
        unilist['Score'].append(score)   
        
    #Get page's information-indicator ----------------------------------------
    dropdowns = driver.find_elements(By.CLASS_NAME,'head-bg')
    driver.execute_script("arguments[0].click();", dropdowns[-1])
    driver.find_element(By.CLASS_NAME, 'rk-tooltip')
    lis = driver.find_elements(By.CSS_SELECTOR, 'li')
    indicator_list = ['Q1', 'CNCI', 'IC', 'TOP', 'AWARD']
    lis[:] = [i for i in lis if i.text in indicator_list]
    for i in lis:
        ind = i.text
        actions = ActionChains(driver)
        actions.move_to_element(i).click().perform()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        items = soup.find_all("tr")
        for row in items[1:]:
            ind_score = row.contents[4].text.lstrip().rstrip()
            unilist[ind].append(ind_score)
        if i in lis[:-1]:
            dropdowns = driver.find_elements(By.CLASS_NAME,'head-bg')
            driver.execute_script("arguments[0].click();", dropdowns[-1])

            

#Crawl a Subject & go through all pages--------------------------------------
def crawl_a_subject(link): 
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    max_pages = int(soup.select(".ant-pagination-item")[-1].text)
    count = 0
    print("---Total page: ", max_pages)
    while(count < max_pages):    
        print('Page: ', count+1, '/', max_pages)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        get_a_page_data(soup)
        next_page = driver.find_elements(By.CLASS_NAME,'ant-pagination-item-link')
        next_page[-1].click()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        count += 1
        time.sleep(1)
    return unilist




#Main------------------------------------------------------------------------
for s in range(len(subject_list)):
    
    unilist = {}
    unilist = {'Institution_Name': [], 'Score': [], 'Rank': [],
           'Q1': [], 'CNCI': [], 'IC': [], 'TOP': [], 'AWARD': []}
    subject = subject_list[s]
    subject_area = subject_area_map[subject][0]
    subject_link = subject_area_map[subject][1] 
    print(f"{subject}  [{s+1} / {len(subject_list)}]")
    
    crawl_a_subject(subject_link)   
    
    df = pd.DataFrame(unilist)
    df["Year"] = "2022"
    df["Subject"] = subject
    df["Area"] = subject_area
    df["Link"] = subject_link
    
    df.to_csv(f"ARWU_by_subject_2022/{subject}.csv", index=False, encoding='utf-8')
    print("- write finish -")
    print("                ")

print("- done -")    
driver.quit()
